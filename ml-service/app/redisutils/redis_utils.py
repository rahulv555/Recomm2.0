import redis
import json
import psycopg2
from .schema import get_places_schema
from redisvl.index import SearchIndex
from app.dbquery import execute_db_query
from redis.commands.json.path import Path
import pandas as pd
from redisvl.query.filter import Tag, Num, Geo, GeoRadius
# from redisvl.query import VectorQuery
import numpy as np

r = redis.Redis(host="recomm_redis", port=6379, decode_responses=False)


def initialise_redis():
    try:
        # The 'DD' argument is the magic part—it deletes the documents too
        r.execute_command("FT.DROPINDEX", "places", "DD")
        print("Dropped index and deleted associated documents.")
    except redis.exceptions.ResponseError:
        print("Index not found, skipping drop.")

    ## SEARCH INDEX FOR PLACES
    places_schema = get_places_schema()
    places_index = SearchIndex(places_schema, redis_client=r)
    places_index.create(overwrite=True, drop=True)

    #Getting the place_id, embeddings, latitude, longitude from DB
    query = "SELECT placeID, latitude, longitude, nn_embedding from places where nn_embedding IS NOT NULL"
    rows = execute_db_query(query)

    columns = ['placeID', 'latitude', 'longitude', 'nn_embedding']

    # Create the DataFrame
    places_df = pd.DataFrame(rows, columns=columns)
    places_df['location'] = places_df.apply(lambda row: f"{row['longitude']},{row['latitude']}", axis=1)
    places_df['nn_embedding'] = places_df['nn_embedding'].apply(lambda x: np.array(x, dtype=np.float32).tolist())
    places_keys = places_index.load(places_df.to_dict(orient='records'))
    

    # FOR USER VECTORS
    query = "SELECT userID, nn_embedding from user_profiles where nn_embedding IS NOT NULL"
    rows = execute_db_query(query)
    columns = ['userID', 'nn_embedding']
    users_df = pd.DataFrame(rows, columns=columns)
    

    with r.pipeline(transaction=False) as pipe:
        for _, row in users_df.iterrows():
            user_key = f"user:{row['userID']}"
            # Keep as list for JSON storage
            user_data = {"user_embedding": np.array(row['nn_embedding'], dtype=np.float32).tolist()}
            pipe.json().set(user_key, "$", user_data)
        pipe.execute()


    sync_untrained_count()
    


    return

def get_restaurants(user_id, filter, num_results=10): #pass the geo filter
    try:
        user_vector = get_user_embedding(user_id)
        print(f"User_vector:{user_vector}")
        if user_vector is None:
            raise ValueError(f"User embedding for {user_id} not found.")
        
        user_vector = np.array(user_vector, dtype=np.float32).tobytes()
        print(type(user_vector))
        print(len(user_vector)) 

        # query = VectorQuery(vector=user_vector,
        #                 vector_field_name='nn_embedding',
        #                 num_results=num_results,
        #                 return_score=True,
        #                 return_fields=['placeID'],
        #                 filter_expression=filter,
        #                 dialect=3
        #                 )
        
        # places_schema = get_places_schema()
        # places_index = SearchIndex(places_schema, redis_client=r)
        # places_index = SearchIndex.from_existing("places", redis_client=r)
        # results = places_index.search(query)


        query = f"{filter}=>[KNN {num_results} @nn_embedding $vec AS score]"

        results = r.execute_command(
            "FT.SEARCH",
            "places",
            query,
            "PARAMS", 2, "vec", user_vector,
            "SORTBY", "score",
            "RETURN", 2, "placeID", "score",
            "DIALECT", 2
        )

        results = parse_recomm_results(results)

        return results
    #can now be accessed by iterating and then using ['nn_embedding']
    except Exception as e:
        print(e)

def parse_recomm_results(redis_result):
    count = redis_result[0]
    results = []

    for i in range(1, len(redis_result), 2):
        key = redis_result[i].decode()
        fields = redis_result[i+1]

        obj = {}
        for j in range(0, len(fields), 2):
            field = fields[j].decode()
            value = fields[j+1].decode()
            obj[field] = value

        obj["redis_key"] = key
        results.append(obj)

    return results

def store_user_embedding(user_id, embedding):
    payload = {"user_embedding": embedding.tolist()}
    r.json().set(f"user:{user_id}", "$", payload)

def get_user_embedding(user_id):
    # .json().get() returns the actual dict, not a string
    data = r.json().get(f"user:{user_id}")
    if data:
        return np.array(data["user_embedding"], dtype=np.float32)
    return None



def get_geo_filter(user_long,
               user_lat,
               radius=10000,
               low_price=0.0,
               high_price=5.0,
               rating=0.0,
               cuisines=[]):
    return f"@location:[{user_long} {user_lat} {radius} m]"
    geo_filter = Geo("location") == GeoRadius(user_long, user_lat, radius, unit="m") # use a distance unit of meters

    # open_filter = Num(f"{current_date_time.strftime('%A').lower()}_open") < current_date_time.hour*100 + current_date_time.minute
    # close_filter = Num(f"{current_date_time.strftime('%A').lower()}_close") > current_date_time.hour*100 + current_date_time.minute
    # time_filter = open_filter & close_filter

    # price_filter = (Num('price') >= low_price) & (Num('price') <= high_price)

    # rating_filter = Num('rating') >= rating

    # cuisine_filter = Tag('cuisine') == cuisines

    # return geo_filter & time_filter & price_filter & rating_filter & cuisine_filter
    return geo_filter


def sync_untrained_count():
    query = "SELECT count(*) from interactions where trained=FALSE"
    rows = execute_db_query(query)
    
    
    # Extract the number from [(count,)]
    untrained_count = rows[0][0]
    
    # Store in Redis as a simple string/int key
    r.set("stats:untrained_interactions", untrained_count)
    return untrained_count

def increment_untrained_count(amount=1):
    # Atomically increment the count in Redis
    # This is great for when a new interaction happens in real-time
    return r.incrby("stats:untrained_interactions", amount)

def get_untrained_count():
    count = r.get("stats:untrained_interactions")
    return int(count) if count else 0

def set_untrained_count_zero():
    r.set("stats:untrained_interactions", 0)
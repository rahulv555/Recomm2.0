import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sentence_transformers import SentenceTransformer
from joblib import dump
import os
import psycopg2






CURRENT_YEAR = 2026


geoplacesdata = pd.read_csv('dataset/geoplaces2.csv')
parkingdata = pd.read_csv('dataset/chefmozparking.csv')
cuisinedat = pd.read_csv('dataset/chefmozcuisine.csv')

#Dropping columns that wouldn't really affect ratings
geoplacesdata = geoplacesdata.drop(columns=['other_services','url','zip','fax','the_geom_meter'])

cuisinedat_agg = (
    cuisinedat
    .groupby('placeID')['Rcuisine']
    .agg(lambda x: list(x.dropna().unique()))
    .reset_index()
)

geoplacesdata = pd.merge(geoplacesdata,parkingdata, on='placeID', how='left')
geoplacesdata = pd.merge(geoplacesdata, cuisinedat_agg, on='placeID', how='left')
geoplacesdata['placeID'] = geoplacesdata['placeID'].astype(str)

# Replacing ? with null
total_data = geoplacesdata.copy()

total_data = total_data.replace('?', np.nan)

# joining name adress etc to create single column
cols = ['name','address','city','state','country']
total_data['final_name'] = total_data[cols].fillna('').agg(', '.join, axis=1)


#List of nominal vars(cuisine) embedding
# For cuisine - list column
#Could try with MultiLabelEncoder


total_data['Rcuisine'] = total_data['Rcuisine'].apply(lambda d: d if isinstance(d, list) else [])

all_cuisines = sorted({c for row in total_data['Rcuisine'] for c in row})

cuisine_le = LabelEncoder()
cuisine_le.fit(all_cuisines)

total_data['cuisine_ids'] = total_data['Rcuisine'].apply(
    lambda x: cuisine_le.transform(x).tolist()
)# list of cuisine ids now, instead of list of cuisines

num_cuisines = len(cuisine_le.classes_)


#ORDINAL VARS embedding
price_map = {
    'low': 0,
    'medium': 1,
    'high': 2
}

total_data['price_ord'] = total_data['price'].map(price_map)
total_data['price_ord'] = total_data['price_ord'] / 3.0

dress_map = {
    'informal': 0,
    'casual': 1,
    'formal': 2
}

total_data['dress_ord'] = total_data['dress_code'].map(dress_map)
total_data['dress_ord'] = total_data['dress_ord'] / 3.0

accessibility_map = {
    'no_accessibility' : 0,
    'partially':1,
    'completely':2
}

total_data['accessibility_ord'] = total_data['accessibility'].map(accessibility_map)
total_data['accessibility_ord'] = total_data['accessibility_ord'] / 3.0

alcohol_map = {
    'No_Alcohol_Served':0,
    'Wine-Beer':1,
    'Full_Bar':2,
}

total_data['alcohol_ord'] = total_data['alcohol'].map(alcohol_map)

total_data['alcohol_ord'] = total_data['alcohol_ord'] / 3.0


## BINARY ENCODING

total_data['is_franchise'] = (total_data['franchise'] == 't').astype(int)
total_data['is_open'] = (total_data['area'] == 'open').astype(int)


## NOMINAL ENCODING


def label_encode(col):
    le = LabelEncoder()
    total_data[col + '_id'] = le.fit_transform(total_data[col].astype(str))
    return le

smoking_le = label_encode('smoking_area')
ambience_le = label_encode('Rambience')
parking_le = label_encode('parking_lot')


## ADDING RATINGS
# Created merged df with the review for the places
ratings_data = pd.read_csv('dataset/rating_final.csv')
ratings_data['placeID'] = ratings_data['placeID'].astype(str)
rating_cols = ['rating', 'food_rating', 'service_rating']

place_stats = (
    ratings_data
    .groupby('placeID')[rating_cols]
    .agg(['count', 'min', 'max', 'mean'])
    .reset_index()
)

# flatten column names
place_stats.columns = [
    'placeID',
    'rating_count', 'rating_min', 'rating_max', 'rating_mean',
    'food_count', 'food_min', 'food_max', 'food_mean',
    'service_count', 'service_min', 'service_max', 'service_mean'
]

global_means = ratings_data[rating_cols].mean()

#bayesian smoothing
m = 10  # smoothing strength

for col in ['rating', 'food', 'service']:
    place_stats[f'{col}_bayes'] = (
        (place_stats[f'{col}_count'] * place_stats[f'{col}_mean'] +
         m * global_means[col if col=='rating' else f'{col}_rating'])
        / (place_stats[f'{col}_count'] + m)
    )


#Normalizing
rating_features = [
    c for c in place_stats.columns
    if c.endswith(('min', 'max', 'mean', 'bayes'))
]

place_stats[rating_features] = place_stats[rating_features] / 5.0


count_cols = ['rating_count', 'food_count', 'service_count']

place_stats[count_cols] = np.log1p(place_stats[count_cols])

total_data = total_data.merge(place_stats, on='placeID', how='left')



## USER DATA
userprofile_data = pd.read_csv('dataset/userprofile.csv')
usercuisine_data= pd.read_csv('dataset/usercuisine.csv')

usercuisinedat_agg = (
    usercuisine_data
    .groupby('userID')['Rcuisine']
    .agg(lambda x: list(x.dropna().unique()))
    .reset_index()
)
userprofile_data = pd.merge(userprofile_data, usercuisinedat_agg, on='userID', how='left')

userprofile_data['age'] = CURRENT_YEAR - userprofile_data['birth_year']
userprofile_data = userprofile_data.replace('?', np.nan)

for col in userprofile_data.columns:
    if col=='Rcuisine':
        continue
    mode = userprofile_data[col].mode()[0]
    userprofile_data[col] = userprofile_data[col].fillna(mode)


## LIST OF NOMINAL VARS
# For cuisine - list column
#Could try with MultiLabelEncoder

userprofile_data['Rcuisine'] = userprofile_data['Rcuisine'].apply(lambda d: d if isinstance(d, list) else [])

all_cuisines = sorted({c for row in userprofile_data['Rcuisine'] for c in row})

usercuisine_le = LabelEncoder()
usercuisine_le.fit(all_cuisines)

userprofile_data['cuisine_ids'] = userprofile_data['Rcuisine'].apply(
    lambda x: usercuisine_le.transform(x).tolist()
)# list of cuisine ids now, instead of list of cuisines

num_usercuisines = len(usercuisine_le.classes_)

#ORDINAL VARS

drinklevel_map = {
    'abstemious': 0,
    'social drinker': 1,
    'casual drinker': 2
}

userprofile_data['drink_level_ord'] = userprofile_data['drink_level'].map(drinklevel_map)
userprofile_data['drink_level_ord'] = userprofile_data['drink_level_ord'] / 3.0

budget_map = {
    'low': 0,
    'medium': 1,
    'high': 2
}

userprofile_data['budget_ord'] = userprofile_data['budget'].map(budget_map)
userprofile_data['budget_ord'] = userprofile_data['budget_ord'] / 3.0

# BOOLEAN
userprofile_data['is_smoker'] = (userprofile_data['smoker'] == 'true').astype(int)

#NOMINAL VARS
def label_encode_users(col):
    le = LabelEncoder()
    
    userprofile_data[col + '_id'] = le.fit_transform(userprofile_data[col].astype(str))
    return le

dress_preference_le = label_encode_users('dress_preference')
userambience_le = label_encode_users('ambience')
transport_le = label_encode_users('transport')
marital_le = label_encode_users('marital_status')
hijos_le = label_encode_users('hijos')
interest_le = label_encode_users('interest')
personality_le = label_encode_users('personality')
religion_le = label_encode_users('religion')
activity_le = label_encode_users('activity')

#Nomalizing with z-score normalisation
heightscaler = StandardScaler()
weightscaler = StandardScaler()
agescaler = StandardScaler()

userprofile_data['height_norm'] = heightscaler.fit_transform(
    userprofile_data[['height']]
)

userprofile_data['weight_norm'] = weightscaler.fit_transform(
    userprofile_data[['weight']]
)

userprofile_data['age_norm'] = agescaler.fit_transform(
    userprofile_data[['age']]
)





### BERT EMBEDDINGS

# Loading BERT model
model = SentenceTransformer('./models/all-MiniLM-L6-v2') 

def safe(x):
    return "" if pd.isna(x) else str(x)

def build_text_groups(row):
    location = (
        f"{safe(row['name'])}. Located at "
        f"{safe(row['address'])}, {safe(row['city'])}, "
        f"{safe(row['state'])}, {safe(row['country'])}."
    )

    attributes = (
        f"Alcohol: {row['alcohol']}. "
        f"Smoking: {row['smoking_area']}. "
        f"Dress code: {row['dress_code']}. "
        f"Accessibility: {row['accessibility']}. "
        f"Price range: {row['price']}. "
        f"Ambience: {row['Rambience']}."
    )

    business = (
        f"Franchise: {row['franchise']}. "
        f"Area: {row['area']}. "
        f"Parking: {row['parking_lot']}."
    )

    cuisines = row['Rcuisine']
    cuisine = (
        "Cuisines: " + ", ".join(cuisines)
        if isinstance(cuisines, list) else "Cuisines:"
    )

    return location, attributes, business, cuisine


final_bert_embs = []

for _, row in total_data.iterrows():
    loc, attr, biz, cui = build_text_groups(row)

    loc_e = model.encode(loc, normalize_embeddings=True)
    attr_e = model.encode(attr, normalize_embeddings=True)
    biz_e = model.encode(biz, normalize_embeddings=True)
    cui_e = model.encode(cui, normalize_embeddings=True)

    final_emb = np.concatenate(
        [loc_e, attr_e, biz_e, cui_e]
    )  # shape: (1536,)

    final_bert_embs.append(final_emb)

total_data['bert_embedding'] = final_bert_embs





## USER BERT EMBEDDINGS
def build_user_text_groups(row):
    lifestyle = " ".join(filter(None, [
        f"Smoker : {row['smoker']},",
        f"Drink level : {row['drink_level']},",
        f"Transport : {row['transport']},",
        f"Activity : {row['activity']},",
    ]))

    social = " ".join(filter(None, [
        f"Marital status : {row['marital_status']},",
        f"Hijos : {row['hijos']},",
        f"Personality : {row['personality']},",
        f"Interest : {row['interest']},",
        f"Religion : {row['religion']},",
    ]))

    preference = " ".join(filter(None, [
        f"Dress pref : {row['dress_preference']},",
        f"Ambience : {row['ambience']},",
        f"Budget : {row['budget']},",
    ]))

    cuisine = " ".join(row['Rcuisine']) if isinstance(row['Rcuisine'], list) else ""
    cuisine = f"Cuisine : {cuisine}"

    return lifestyle, social, preference, cuisine

final_bert_userembs = []

for _, row in userprofile_data.iterrows():
    life, soci, pref, cuis = build_user_text_groups(row)

    life_e = model.encode(life, normalize_embeddings=True)
    soci_e = model.encode(soci, normalize_embeddings=True)
    pref_e = model.encode(pref, normalize_embeddings=True)
    cuis_e = model.encode(cuis, normalize_embeddings=True)

    final_emb = np.concatenate(
        [life_e, soci_e, pref_e, cuis_e]
    )  # shape: (1536,)

    final_bert_userembs.append(final_emb)

userprofile_data['bert_embedding'] = final_bert_userembs




#################################################################
## SAVING TO DB



conn = psycopg2.connect(database='reco_db', user='reco_user',password='reco_pass')

cur = conn.cursor()

insert_sql = """
INSERT INTO user_profiles (
    userID, latitude, longitude,
    smoker, drink_level, budget, dress_preference, ambience, transport, marital_status, hijos, birth_year, interest, personality, religion, activity, color, weight, height, age,
    rcuisine, cuisine_ids,
    drink_level_ord, budget_ord, is_smoker,
    dress_preference_id, ambience_id, transport_id,
    marital_status_id, hijos_id, interest_id,
    personality_id, religion_id, activity_id,
    height_norm, weight_norm, age_norm,
    bert_embedding
)
VALUES (
    %s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,
    %s,%s,%s,
    %s,%s,%s,
    %s,%s,%s,
    %s,%s,%s,
    %s,%s,%s,
    %s
)
ON CONFLICT (userID) DO NOTHING
"""

for _, row in userprofile_data.iterrows():
    cur.execute(
        insert_sql,
        (
            row.userID,
            float(row.latitude),
            float(row.longitude),

           str(row.smoker),
           str(row.drink_level),
           str(row.budget),
           str(row.dress_preference),
           str(row.ambience),
           str(row.transport),
           str(row.marital_status),
           str(row.hijos),
           int(row.birth_year),
           str(row.interest),
           str(row.personality),
           str(row.religion),
           str(row.activity),
           str(row.color),
           float(row.weight),
           float(row.height),
           float(row.age),

           row.Rcuisine,
           row.cuisine_ids,
          
            float(row.drink_level_ord),
            float(row.budget_ord),
            int(row.is_smoker),

            int(row.dress_preference_id),
            int(row.ambience_id),
            int(row.transport_id),
            int(row.marital_status_id),
            int(row.hijos_id),
            int(row.interest_id),
            int(row.personality_id),
            int(row.religion_id),
            int(row.activity_id),

            float(row.height_norm),
            float(row.weight_norm),
            float(row.age_norm),

            row.bert_embedding.tolist()  # MUST be Python list
        )
    )

conn.commit()




insert_sql = """
INSERT INTO places (
    placeID, latitude, longitude,
    
    name, address, city, state, country, alcohol, smoking_area, dress_code, accessibility, price, rambience, franchise, area, parking_lot,
    rcuisine, cuisine_ids,

    price_ord, dress_ord, accessibility_ord, alcohol_ord,
    is_franchise, is_open,

    smoking_area_id, rambience_id, parking_lot_id,

    rating_count, rating_min, rating_max, rating_mean, rating_bayes,
    food_count, food_min, food_max, food_mean, food_bayes,
    service_count, service_min, service_max, service_mean, service_bayes,

    bert_embedding
)
VALUES (
    %s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,
    %s,%s,%s,%s,
    %s,%s,
    %s,%s,%s,
    %s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,
    %s
)
ON CONFLICT (placeID) DO NOTHING
"""

for _, row in total_data.iterrows():
    cur.execute(
        insert_sql,
        (
            str(row.placeID),
            float(row.latitude),
            float(row.longitude),
            str(row['name']), str(row.address), str(row.city), str(row.state), str(row.country), str(row.alcohol), str(row.smoking_area), str(row.dress_code), str(row.accessibility), str(row.price), str(row.Rambience), str(row.franchise), str(row.area), str(row.parking_lot),
            row.Rcuisine,
            row.cuisine_ids,
            float(row.price_ord),
            float(row.dress_ord),
            float(row.accessibility_ord),
            float(row.alcohol_ord),

            int(row.is_franchise),
            int(row.is_open),

            int(row.smoking_area_id),
            int(row.Rambience_id),
            int(row.parking_lot_id),

            float(row.rating_count) if not np.isnan(row.rating_count) else None,
            float(row.rating_min)   if not np.isnan(row.rating_min) else None,
            float(row.rating_max)   if not np.isnan(row.rating_max) else None,
            float(row.rating_mean)  if not np.isnan(row.rating_mean) else None,
            float(row.rating_bayes) if not np.isnan(row.rating_bayes) else None,

            float(row.food_count) if not np.isnan(row.food_count) else None,
            float(row.food_min)   if not np.isnan(row.food_min) else None,
            float(row.food_max)   if not np.isnan(row.food_max) else None,
            float(row.food_mean)  if not np.isnan(row.food_mean) else None,
            float(row.food_bayes) if not np.isnan(row.food_bayes) else None,

            float(row.service_count) if not np.isnan(row.service_count) else None,
            float(row.service_min)   if not np.isnan(row.service_min) else None,
            float(row.service_max)   if not np.isnan(row.service_max) else None,
            float(row.service_mean)  if not np.isnan(row.service_mean) else None,
            float(row.service_bayes) if not np.isnan(row.service_bayes) else None,

            row.bert_embedding.tolist()  # REQUIRED
        )
    )

conn.commit()




#### SAVING ENCODERS AND SCALERS
os.makedirs("app/artifacts/users/scalers", exist_ok=True)

dump(heightscaler, "app/artifacts/users/scalers/height_scaler.joblib")
dump(weightscaler, "app/artifacts/users/scalers/weight_scaler.joblib")
dump(agescaler,   "app/artifacts/users/scalers/age_scaler.joblib")

os.makedirs("app/artifacts/users/encoders/userencoders", exist_ok=True)

dump(dress_preference_le, "app/artifacts/users/encoders/userencoders/dress_preference_le.joblib")
dump(userambience_le, "app/artifacts/users/encoders/userencoders/userambience_le.joblib")
dump(transport_le,  "app/artifacts/users/encoders/userencoders/transport_le.joblib")
dump(marital_le,  "app/artifacts/users/encoders/userencoders/marital_le.joblib")
dump(hijos_le,  "app/artifacts/users/encoders/userencoders/hijos_le.joblib")
dump(interest_le,  "app/artifacts/users/encoders/userencoders/interest_le.joblib")
dump(personality_le,  "app/artifacts/users/encoders/userencoders/personality_le.joblib")
dump(religion_le,  "app/artifacts/users/encoders/userencoders/religion_le.joblib")
dump(activity_le,  "app/artifacts/users/encoders/userencoders/activity_le.joblib")
dump(usercuisine_le, "app/artifacts/users/encoders/userencoders/usercuisine_le.joblib")


os.makedirs("app/artifacts/users/encoders/placeencoders", exist_ok=True)

dump(smoking_le,  "app/artifacts/users/encoders/placeencoders/smoking_le.joblib")
dump(ambience_le,  "app/artifacts/users/encoders/placeencoders/ambience_le.joblib")
dump(parking_le,  "app/artifacts/users/encoders/placeencoders/parking_le.joblib")
dump(cuisine_le,  "app/artifacts/users/encoders/placeencoders/cuisine_le.joblib")




## Load interactions
data = pd.read_csv('dataset/rating_final.csv')
data.head()


cur = conn.cursor()


insert_sql = """
INSERT INTO interactions (
    placeID, userID, rating, food_rating, service_rating, trained
)
VALUES (
    %s,%s,%s,%s,%s,%s
)
ON CONFLICT (userID, placeID) DO NOTHING
"""

for _, row in data.iterrows():
    cur.execute(
        insert_sql,
        (   
            str(row.placeID),
            row.userID,
            float(row.rating),
            float(row.food_rating),
            float(row.service_rating),
            True
     
        )
    )

conn.commit()
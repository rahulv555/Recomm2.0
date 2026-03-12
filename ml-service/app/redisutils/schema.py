from redisvl.schema import IndexSchema


# Store place latitude, longitude, nn_embeddings

def get_places_schema():
    places_schema = IndexSchema.from_dict({
        'index' : {
            'name' : 'places',
            'prefix' :['places'],
            'storage_type' : 'json'
        },
        'fields' : [
            {
                'name': 'nn_embedding',
                'type': 'vector',
                'attrs': {
                    'dims': 128, 
                    'algorithm': 'flat',
                    'datatype': 'float32',
                    'distance_metric': 'cosine'
                }
            },
            {'name': 'location', 'type': 'geo'},
            {'name': 'placeID', 'type': 'tag'}

            # can add other filters here     

        ]
        }
        

    )

    return places_schema

    # restaurant_index = SearchIndex(places_schema, redis_client=redis_client)
    # restaurant_index.create(overwrite=True, drop=True) 



    # # restaurant_keys = restaurant_index.load(df.to_dict(orient='records'))
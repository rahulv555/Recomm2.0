-- db/init.sql

CREATE TABLE IF NOT EXISTS user_profiles (
    
    userID TEXT PRIMARY KEY,
    name VARCHAR,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    smoker VARCHAR,
    drink_level VARCHAR,
    budget VARCHAR,
    dress_preference VARCHAR,
    ambience VARCHAR,
    transport VARCHAR,
    marital_status VARCHAR,
    hijos VARCHAR,
    birth_year INTEGER,
    interest VARCHAR,
    personality VARCHAR,
    religion VARCHAR,
    activity VARCHAR,
    color VARCHAR,
    weight DOUBLE PRECISION,
    height DOUBLE PRECISION,
    rcuisine VARCHAR[],
    age INTEGER,

    cuisine_ids INTEGER[],
    drink_level_ord DOUBLE PRECISION,
    budget_ord DOUBLE PRECISION,
    is_smoker INTEGER,

    dress_preference_id INTEGER,
    ambience_id INTEGER,
    transport_id INTEGER,
    marital_status_id INTEGER,
    hijos_id INTEGER,
    interest_id INTEGER,
    personality_id INTEGER,
    religion_id INTEGER,
    activity_id INTEGER,
    

    height_norm DOUBLE PRECISION,
    weight_norm DOUBLE PRECISION,
    age_norm DOUBLE PRECISION,

    bert_embedding FLOAT8[],

    nn_embedding FLOAT8[]
);

CREATE TABLE IF NOT EXISTS places (
    placeID VARCHAR PRIMARY KEY,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,

    name VARCHAR,
    address VARCHAR,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    alcohol VARCHAR,
    smoking_area VARCHAR,
    dress_code VARCHAR,
    accessibility VARCHAR,
    price VARCHAR,
    rambience VARCHAR,
    franchise VARCHAR,
    area VARCHAR,
    parking_lot VARCHAR,
    Rcuisine VARCHAR[],

    cuisine_ids INTEGER[],
    price_ord DOUBLE PRECISION,
    dress_ord DOUBLE PRECISION,
    accessibility_ord DOUBLE PRECISION,
    alcohol_ord DOUBLE PRECISION,

    is_franchise INTEGER,
    is_open INTEGER,

    smoking_area_id INTEGER,
    rambience_id INTEGER,
    parking_lot_id INTEGER,

    rating_count DOUBLE PRECISION,
    rating_min DOUBLE PRECISION,
    rating_max DOUBLE PRECISION,
    rating_mean DOUBLE PRECISION,
    rating_bayes DOUBLE PRECISION,

    food_count DOUBLE PRECISION,
    food_min DOUBLE PRECISION,
    food_max DOUBLE PRECISION,
    food_mean DOUBLE PRECISION,
    food_bayes DOUBLE PRECISION,

    service_count DOUBLE PRECISION,
    service_min DOUBLE PRECISION,
    service_max DOUBLE PRECISION,
    service_mean DOUBLE PRECISION,
    service_bayes DOUBLE PRECISION,

    bert_embedding FLOAT8[],

    nn_embedding FLOAT8[]
);



CREATE TABLE interactions(
    placeID VARCHAR,
    userID TEXT,
    rating DOUBLE PRECISION,
    food_rating DOUBLE PRECISION,
    service_rating DOUBLE PRECISION,
    trained BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (placeID, userID)
);
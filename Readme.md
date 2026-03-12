1. Setup DB and tables
   Inside db, run setup_reco_postgres.sh

2. Inside ml-service, Run datasetup.py and training.ipynb
   after creating a python 3.12 venv with the requirements.txt

3. Startup api-gateway

4. Startup Kafka

5. Startup ml-service with redis

6. Startup recomm-service

7. Startup User-service

8. Startup restaurant-service

APIGATEWAY - 4005
ML-SERVICE - 8088
DB - 5432
REDIS - 6372
RECOMM - 8087
RESTAURANT - 8086
USER - 8085

ENDPOINTS -
/api/users/ - GET - Get specific user
{
RESPONSE :
STRINGS - "name","smoker","drink_level","budget","dress_preference","ambience","transport","marital_status","hijos","personality","religion","interest",activity","color"
LIST STRINGS - "cuisine"
DOUBLE - "height","weight"
INT - "birth_year","age"

}
/api/users/exists - GET - Get if user exists
{
RESPONSE :
BOOLEAN "userExists"
}
/api/users/create - POST - Create user
{
REQUEST and RESPONSE:
STRINGS - "name","smoker","drink_level","budget","dress_preference","ambience","transport","marital_status","hijos","personality","religion","interest",activity","color"
LIST STRINGS - "cuisine"
DOUBLE - "height","weight"
INT - "birth_year","age"

RESPONSE:

}
/api/users/rate - POST - Rate a place
{
REQUEST and RESPONSE:
"placeID" - STRING
DOUBLE = "rating","foodRating","serviceRating"
}
/api/users/update - PATCH - Update User
{
REQUEST:
STRINGS - "smoker","drink_level","budget","dress_preference","ambience","transport","marital_status","hijos","personality","religion","interest",activity","color"
LIST STRINGS - "cuisine"
DOUBLE - "height","weight"

        RESPONSE:
        Nothing
    }

/api/restaurant/ - POST - Get specfic restaurant
{
REQUEST:
"placeID" = string

RESPONSE:
DOUBLE - "latitude", "longitude"
STRING - name, address, state, country, alcohol, smoking_area, dress_code, accessibility, price, rambience, franchise, area, parking_lot
LIST OF STRINGS - Rcuisine

}
/api/restaurant/list - POST - Get list of restaurants
{
REQUEST
"placeIDs" = List of strings

RESPONSE - List of below
DOUBLE - "latitude", "longitude"
STRING - name, address, state, country, alcohol, smoking_area, dress_code, accessibility, price, rambience, franchise, area, parking_lot
LIST OF STRINGS - Rcuisine

}

/api/restaurant/rates - GET - Get Ratings made by a user
RESPONSE :
List of below
Double - rating, foodrating, serviceRating
String - name, placeID

/api/recomm/ - POST - Get Recommendations
{
REQUEST
Double - "Latitude" "Longitude"

RESPONSE
List of String - placeIds

}



npm create vite@5 restaurant-frontend -- --template react
npm install
npm install firebase leaflet react-leaflet@^4.2.1
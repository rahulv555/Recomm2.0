# Subtitle Generator

This is a Restaurant recommendation system, that generates recommendations for a user based on their and other's profile, preferences, location and interactions, using a neural network based Two-Tower Recommendation System. The entire system has been created with a microservices-based architecture, using springboot for all service except the ML-service, which uses python FastApi. For storage, PostgresDB is used and for cache/vector-search, Redis is used. For showcasing the system, I have created a basic React-based Web UI, that allows accessing all the endpoints to test the system.

## The Two Tower Recommendation Model


## The System architecture


## How to setup
Startup Docker Desktop or equivalent to start the docker engine, before proceeding
### 0. Setup Firebase
Setup Firebase Auth with email/password verification, and download the firebase-service-account.json to apigateway/apigateway/src/main/resources

### 1. Setup DB and tables
Edit the value of VOLUME in db/setup_reco_postgres.sh to the directory you wish to store the data
Once docker is up, inside db directory, run setup_reco_postgres.sh to setup the db and create the tables(inside init_reco.sql)
````bash
cd db
./setup_reco_postgres.sh
````

### 2. Setup the data and train the Two Tower NN model
Once DB is up and running with the tables created, for the next step, a python 3.12 virtualenv is required, using the packages mentioned in ml-service/requirements.txt
````bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r ml-model/requirements.txt
````
To setup the data, once the env is activated
````bash
cd ml-service
python datasetup.py
````
This will load the data from the dataset directory, clean it up, do feature engineering, encoding, scaling and then store the entire data in the DB.
All the encoders and scalers created are stored as .joblib files in the app/artifact directory.
BERT embeddings(using all-MiniLM-L6-v2 stored in models) are also created, to be passed parallely with the other encoded features

Once the data is loaded, next step is to train the model. The Two Tower model definition is stored in app/model/model.py
For this step, run the cells in **training.ipynb**. This will train the model, with schedulers and optimizers, and retrain with the validation data to create a separate model, and store both models (.pt) for future use under models/twotower.
The place/restaurant embeddings are also generated with the PlaceTower and stored in DB (as they don't have to be recalculated again)

3. Startup Kafka
````bash
./setup-kafka.sh
````
Creates network reco-network. Starts kafka on port 9092

5. Setup remaining services
Run setup-all.sh to setup the remaining services. If this fails, run individual setup.sh inside each service directory
````bash
./setup-all.sh
````
The services startup inside reco-network with the following ports
**APIGATEWAY - 4005
ML-SERVICE - 8088
DB - 5432
REDIS - 6372
RECOMM-SERVICE - 8087
RESTAURANT-SERVICE - 8086
USER-SERVICE - 8085**


## ENDPOINTS -
All requests to http://localhost:4005/api/ (apigateway) need the Bearer <valid firebase auth token> Authorization header, will be filtered using a TokenAuthFilter in the apigateway, which verifies the Bearer <Token> authorization header with firebase, and if valid, adds the X-Authenticated-User-Id header to requests before forwarding them

#### Refer endpoints.txt to see endpoints exposed from apigateway


## FRONTEND / WEB UI
Run the following
````bash
npm create vite@5 restaurant-frontend -- --template react
npm install
npm install firebase leaflet react-leaflet@^4.2.1
npm run dev
````

#### 1. Login / Signup Page
<img width="1638" height="941" alt="login" src="https://github.com/user-attachments/assets/5465f09c-17f7-4754-9b2a-c9a85ba70338" />

#### 2. Create profile
<img width="1858" height="903" alt="NewProfile" src="https://github.com/user-attachments/assets/668140ee-efe4-41d2-bbc4-c4ade1dd1ff1" />


Appears when signing in for the first time. User must fill all details and save, before being able to get recommendations

#### 3. Filled and Save profile
<img width="1852" height="924" alt="FilledProfile2" src="https://github.com/user-attachments/assets/4e1008de-0cf9-4c9b-960e-0074612337d6" />


A filled profile, that can be saved. This stores the profile to DB, and triggers the user embedding creation, which gets stored in Redis as well.
This can be edited and saved, which reinvokes the creation of the updated user embedding.

#### 4. Select location for recommendation
<img width="1858" height="953" alt="MapBeforeRecomm" src="https://github.com/user-attachments/assets/2cd4fb23-cd26-4216-bc0b-b15cd09cc892" />


User can click to place red marker, select location and click on the button for recommendation. This invokes a Vector search using cosine similiarity with the place/restaurant embeddings stored in Redis, with the user embedding(which is the same as the inference step of the Two Tower model), along with a GeoFilter applied.

The user's past ratings are also shown


#### 5. Recommendation result
<img width="1854" height="939" alt="Recomm" src="https://github.com/user-attachments/assets/d915415e-ba4b-4e37-8294-38a3ba98e35a" />

The recommended places are shown on the map with blue marker. Clicking on them shows their details in the sidebar




#### 6. Rating a place
<img width="1857" height="927" alt="Rating" src="https://github.com/user-attachments/assets/327fa157-ca91-4473-bd9e-7deb4202fdeb" />

If the place has been rated previously by the user, that rating is shown as the preset value
Adjust the slider to place the rating (Can be replaced with a star system, currently the slider moves in 0.5 steps)
Click on save rating. This adds this interaction to the DB, and once the number of untrained interactions crosses a threshold, the model is retrained with these new interactions.

#### 7. After rating
<img width="1852" height="941" alt="Rated" src="https://github.com/user-attachments/assets/9eb8833a-fa42-42fe-bbcb-9a21c6c68f50" />

The interaction is added to the user's history

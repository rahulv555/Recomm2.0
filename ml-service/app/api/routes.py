from fastapi import APIRouter, BackgroundTasks, HTTPException
import numpy as np
from pydantic import BaseModel
import torch
from pathlib import Path
from app.model.inference import Recommender
import app.redisutils.redis_utils as rd
from app.dbquery import execute_db_query


router = APIRouter()

# Resolve paths relative to the ml-service root so imports work regardless of CWD
BASE_DIR = Path(__file__).resolve().parents[2]

recommender = Recommender(
    model_path=str(BASE_DIR / "models"),
    encoder_dir=str(BASE_DIR / "app" / "artifacts" / "users" / "encoders" / "userencoders"),
    scalers_dir=str(BASE_DIR / "app" / "artifacts" / "users" / "scalers"),
)

UNTRAINED_THRESHOLD = 32

class RecommendRequest(BaseModel):
    longitude: float
    latitude: float

# Return list of place IDs, based on a userID
@router.post("/recommend")
def recommend(user_id: str, request: RecommendRequest):
    print(request)
    lat= request.latitude
    long = request.longitude
    user_vector = rd.get_user_embedding(user_id)
    
    if user_vector is None:
        # Fallback if user is new/not in Redis
        #Fetch from DB
        db_res = execute_db_query("SELECT nn_embedding FROM user_profiles WHERE userID = %s", (user_id,))
        if not db_res:
            raise HTTPException(status_code=404, detail="User not found")
        user_vector = np.array(db_res[0][0], dtype=np.float32)

    
    geo_filter = rd.get_geo_filter(long, lat, radius=20000)

    results = rd.get_restaurants(user_id, geo_filter)

    return {"recommendations": [res["placeID"] for res in results]}

    #Cosine similiarity search via redis is simliar to the final inference layer in the two tower model


# Train model with new interactions, if number of untrained interactions has crossed threshold (checked here)
@router.post("/liketrain")
def likeTrain(background_tasks: BackgroundTasks):
    untrained_count = rd.get_untrained_count()
    if untrained_count > UNTRAINED_THRESHOLD:

        rd.set_untrained_count_zero() #to prevent multiple liketrains

        background_tasks.add_task(recommender.retrain_on_new_interactions)

        
        

        return {"status": "retrained"}
    else:
        rd.increment_untrained_count()
        return {"status": "incremented", "current": untrained_count + 1}

   


# When user is created/edited
@router.post("/usertrain")
def userTrain(user_id: str):
    # 1. Pull new data from Postgres
    # 2. Encode the appropriate columns using the saved encoders
    # 3. Run through UserTower to get new embedding
    # 4. Update Redis JSON
    try:
        nn_vector = recommender.update_single_user_embedding(user_id)
        if nn_vector is None:
            raise HTTPException(status_code=404, detail="User not found in Postgres")
        print(nn_vector[:5])
        return {"status": "user_updated"}

    except Exception as e:
        print(f"Error during usertrain: {e}")
        raise HTTPException(status_code=500, detail=str(e))
   
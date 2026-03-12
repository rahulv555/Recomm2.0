from fastapi import FastAPI
from app.api.routes import router
from app.redisutils.redis_utils import initialise_redis



app = FastAPI()

app.include_router(router)


# # Initialise embeddings from DB to redis
# @app.on_event("startup")
# def on_startup():
#     initialise_redis()

@app.get("/")
def health():
    return {"status": "ml-service-running"}


# uvicorn app.main:app --reload --port 8000 --workers 4
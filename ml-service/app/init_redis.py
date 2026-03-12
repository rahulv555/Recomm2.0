from app.redisutils.redis_utils import initialise_redis

if __name__ == "__main__":
    print("Pre-start: Initializing Redis...")
    initialise_redis()
    print("Pre-start: Redis ready.")
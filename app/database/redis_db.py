from redis.asyncio import Redis
from app.config import settings

__redis_url = settings.REDIS_URL

redis_db = Redis.from_url(url=__redis_url,decode_responses = True)

#add to db 
async def blacklist_jti(jti : str):
    return await redis_db.set(jti,"blacklisted")

#verify jwt
async def check_blacklisted(jti:str):
    return await redis_db.exists(jti)


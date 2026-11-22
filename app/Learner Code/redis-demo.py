from app.config import settings 
from redis import Redis
import secrets

__redis_url = settings.REDIS_URL
blacklist = Redis.from_url(url=__redis_url,decode_responses = True)
s1 = secrets.token_hex(8)
print(f"s1 : {s1}")
t1 = 45
blacklist.set(f"sec","revoked",ex=t1)
res = blacklist.get("sec") # if not decode_responses we get b'revoked'
print(res)
print(blacklist.exists('sec'))
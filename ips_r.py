import redis
from log_ import log
from config import *

class RedisClient(object):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        self.db=redis.StrictRedis(host=host,port=port,password=password)
    def add(self,proxy):
        if not self.db.sismember(REDIS_KEY,proxy):
            log.info('already insert'+proxy)
            return self.db.sadd(REDIS_KEY,proxy)
    def decrease(self,proxy):
        log.info('already remove'+proxy)
        return self.db.srem(REDIS_KEY,proxy)
    def random(self,num=1):
        try:
            return self.db.srandmember(REDIS_KEY,num)
        except:
            return self.db.smembers(REDIS_KEY)
    def count(self):
        return self.db.scard(REDIS_KEY)
    def get_all(self):
        return self.db.smembers(REDIS_KEY)
def save(proxy):
    redis=RedisClient()
    redis.add(proxy)
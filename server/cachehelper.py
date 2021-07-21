from datetime import time
import redis
import json
import time


class CacheProvider():
    def __init__(self, redis_host, redis_port):
        self.connection = redis.Redis(redis_host, redis_port)

    def setCache(self, key, value):
        self.connection.set(key, value)

    def setCacheJson(self, key, jsonObj):
        json_str = json.dumps(jsonObj)
        self.connection.set(key, json_str)

    def getCache(self, key):
        try:
            return self.connection.get(key)
        except:
            # TODO Log Failure
            return None

    def getCachedJson(self, key):
        try:
            obj = self.connection.get(key)
            if(obj is not None):
                jsonObj = json.loads(obj)
                return jsonObj
        except:
            # TODO Log Failure
            return None

    def getCacheWithRetry(self, key, timeout):
        counter = 0
        while counter < timeout:
            obj = self.getCache(key)
            if(obj is not None):
                return obj
            else:
                time.sleep(1)
            counter = counter+1

    def getCachedJsonWithRetry(self, key, timeout):
        counter = 0
        while counter < timeout:
            obj = self.getCachedJson(key)
            if(obj is not None):
                return obj
            else:
                time.sleep(1)
            counter = counter+1

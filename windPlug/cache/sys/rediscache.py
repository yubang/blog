# coding:UTF-8


"""
缓存模块
@author:yubang
"""


from django.core.cache.backends.base import BaseCache
import redis
import json


class RedisCache(BaseCache):
    """基于redis的django缓存模块"""
    def __init__(self, server, param):
        host = param.get('host', 'localhost')
        port = param.get('port', 6379)
        db = param.get('db', 0)
        self.timeout = param.get('timeout', 1800)
        self.key_prefix = param.get('key_prefix', 'windPlug')
        self.__cache = redis.Redis(host=host, port=port, db=db)

    def __del__(self):
        pass

    def make_key(self, key, version=None):
        if version is None:
            version = 'default'
        else:
            version = str(version)
        return '_'.join((self.key_prefix, version, key))

    def has_key(self, key, version=None):
        return self.__cache.get(key) is not None

    def set(self, key, value, timeout=None, version=None):
        if timeout is None:
            timeout = self.timeout
        self.__cache.expire(self.make_key(key, version), timeout)

        v = dict()
        v['type'] = type(value).__name__
        v['data'] = value
        return self.__cache.set(self.make_key(key, version), json.dumps(v))

    def get(self, key, default=None, version=None):
        d = self.__cache.get(self.make_key(key, version))

        if d is None:
            return None

        data = json.loads(d)
        return data['data']

    def add(self, key, value, timeout=None, version=None):
        if self.has_key(key):
            return False
        return self.set(key, value, timeout=None, version=None)

    def delete(self, key, version=None):
        return self.__cache.delete(self.make_key(key, version))

    def clear(self):
        return self.__cache.flushdb()

    def close(self, **kwargs):
        pass
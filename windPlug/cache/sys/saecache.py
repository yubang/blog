# coding:UTF-8


"""
缓存模块
@author:yubang
"""


from django.core.cache.backends.base import BaseCache
import json
import time
import sae.kvdb


class SaeKVCache(BaseCache):
    """基于sae的django缓存模块"""
    def __init__(self, server, param):
        self.timeout = param.get('timeout', 1800)
        self.key_prefix = param.get('key_prefix', 'windPlug')
        self.__cache = sae.kvdb.Client()

    def __del__(self):
        pass

    def make_key(self, key, version=None):
        if version is None:
            version = 'default'
        else:
            version = str(version)
        return str('_'.join((self.key_prefix, version, key)))

    def has_key(self, key, version=None):
        return self.__cache.get(self.make_key(key, version)) is not None

    def set(self, key, value, timeout=None, version=None):
        if timeout is None:
            timeout = 3600
        v = dict()
        v['type'] = type(value).__name__
        v['data'] = value
        v['time'] = time.time() + timeout
        v = json.dumps(v)
        return self.__cache.set(self.make_key(key, version), v)

    def get(self, key, default=None, version=None):
        d = self.__cache.get(self.make_key(key, version))

        if d is None:
            return None

        data = json.loads(d)
        return data['data']

    def add(self, key, value, timeout=None, version=None):
        if timeout is None:
            timeout = 3600
        v = dict()
        v['type'] = type(value).__name__
        v['data'] = value
        v['time'] = time.time() + timeout
        v = json.dumps(v)
        return self.__cache.add(self.make_key(key, version), v, timeout=None, version=None)

    def delete(self, key, version=None):
        return self.__cache.delete(self.make_key(key, version))

    def clear(self):
        pass

    def close(self, **kwargs):
        self.disconnect_all()
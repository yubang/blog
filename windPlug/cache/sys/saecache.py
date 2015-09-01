# coding:UTF-8


"""
缓存模块
@author:yubang
"""


from django.core.cache.backends.base import BaseCache
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
        return '_'.join((self.key_prefix, version, key))

    def has_key(self, key, version=None):
        return self.__cache.get(self.make_key(key, version)) is not None

    def set(self, key, value, timeout=None, version=None):
        if timeout is None:
            timeout = self.timeout
        self.__cache.expire(self.make_key(key, version), timeout)
        return self.__cache.set(self.make_key(key, version), value)

    def get(self, key, default=None, version=None):
        return self.__cache.get(self.make_key(key, version))

    def add(self, key, value, timeout=None, version=None):
        return self.__cache.add(self.make_key(key, version), value, timeout=None, version=None)

    def delete(self, key, version=None):
        return self.__cache.delete(self.make_key(key, version))

    def clear(self):
        pass

    def close(self, **kwargs):
        self.disconnect_all()
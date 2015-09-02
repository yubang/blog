# coding:UTF-8


"""
页面缓存模块
"""


from django.core.cache import cache
from django.http import HttpResponse
from functools import wraps
import windPlugConfig
import json
import hashlib
import time


def save_data(cache_key, response, cache_timeout):
    """保存数据"""
    data = response.content
    meta = dict()
    meta['Content-Type'] = response['Content-Type']
    cache.set(cache_key, json.dumps({'meta': meta, 'data': data}), cache_timeout)


def get_data(cache_key):
    """获取数据"""
    #尝试从缓存提取内容
    data = cache.get(cache_key)
    if data:
        d = json.loads(data)
        metas = d['meta']
        response = HttpResponse(d['data'])
        response['windPlugCacheHit'] = "on"
        response['windPlugCacheType'] = "page_cache"
        for key in metas:
            response[key] = metas[key]
        return response


def page_cache(session_sign=False, session_key=None, path_sign=False, cookie_sign=False, cookie_key=None, cache_timeout = 3600):
    """
    页面缓存
    cache key构成： session(md5)_cookie(md5)_url(md5)的md5 + 前缀
    @:param session_sign是否通过session来区分是否使用缓存
    @:param path_sign 是否通过路径来判断是否有缓存
    @:param cache_timeout 缓存时间
    """
    def handle(func):
        @wraps(func)
        def deal(*args, **kwds):
            cache_key = ""
            use_cache_sign = True
            request = args[0]
            #处理session类型缓存
            if session_sign:
                session_data = dict()
                for key in session_key:
                    if key not in request.session:
                        use_cache_sign = False
                        break
                    session_data[key] = request.session[key]
                cache_key = cache_key + "session_" + hashlib.md5(json.dumps(session_data)).hexdigest() + "_"

            if cookie_sign:
                cache_key = cache_key + "cookie_" + hashlib.md5(json.dumps(cookie_key)).hexdigest() + "_"
            if path_sign:
                cache_key = cache_key + "path_" + hashlib.md5(args[0].path).hexdigest()
            cache_key = windPlugConfig.PAGE_CACHE_PREFIX + '_' + cache_key

            #获取缓存
            if use_cache_sign:
                response = get_data(cache_key)
                if response:
                    return response

            response = func(*args, **kwds)
            response['windPlugCacheHit'] = "off"
            response['windPlugCacheType'] = "page_cache"

            #保存数据
            save_data(cache_key, response, cache_timeout)

            return response
        return deal
    return handle
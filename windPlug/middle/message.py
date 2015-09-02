# coding:UTF-8


"""
一个仅仅为了输出自定义headers的中间件
@author:yubang
"""


import windPlugConfig


class Message(object):
    def process_response(self, request, response):
        for key in windPlugConfig.OWN_HEADERS:
            response[key] = windPlugConfig.OWN_HEADERS[key]
        return response
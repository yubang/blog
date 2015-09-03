# coding:UTF-8


"""
处理访问的浏览器类型
@author: yubang
"""


import re


def get_browser_data():
    """
    获取浏览器信息
    :return: dict
    """
    datas = [
        {'name': '360浏览器', 'key': '360SE'},
        {'name': 'UC浏览器', 'key': 'UCWEB'},
        {'name': 'UC浏览器', 'key': 'UCBrowser'},
        {'name': 'QQ浏览器', 'key': 'QQBrowser'},
        {'name': 'Firefox浏览器', 'key': 'Firefox'},
        {'name': '搜狗浏览器', 'key': 'SE'},
        {'name': '搜狗浏览器', 'key': 'MetaSr'},
        {'name': '搜狗手机浏览器', 'key': 'SogouMobileBrowser'},
        {'name': 'opera浏览器', 'key': 'opera'},
        {'name': '遨游浏览器', 'key': 'Maxthon'},
        {'name': '百度浏览器', 'key': 'baidubrowser'},

        {'name': '谷歌浏览器', 'key': 'Chrome'},
        {'name': 'IE浏览器', 'key': 'MSIE'},
        {'name': 'Safari浏览器', 'key': 'Safari'},
    ]
    return datas


def is_pc_browser(request=None,user_agent=None):
    """
    是否是pc浏览器
    :param request: django的Request对象
    :param user_agent: 浏览器user-agent
    :return: boolean
    """
    if request:
        user_agent = request.META.get('HTTP_USER_AGENT', None)
    return not re.search(r'Mobile', user_agent)


def get_browser_type(request=None, user_agent=None):
    """
    获取浏览器类型
    :param request: django的Request对象
    :param user_agent: 浏览器user-agent
    :return: str
    """
    if request:
        user_agent = request.META.get('HTTP_USER_AGENT', None)
    browser_data = get_browser_data()
    for data in browser_data:
        if re.search(data['key'], user_agent):
            return data['name']
    return "未知浏览器"


def get_browser_os(request=None, user_agent=None):
    """
    获取客户操作系统
    :param request: django的Request对象
    :param user_agent: 浏览器user-agent
    :return: str
    """
    if request:
        user_agent = request.META.get('HTTP_USER_AGENT', None)
    os_data = [
        {'name': 'Windows 10', 'key': 'Windows NT 6.4'},
        {'name': 'Windows 8.1', 'key': 'Windows NT 6.4'},
        {'name': 'Windows 8', 'key': 'Windows NT 6.4'},
        {'name': 'Windows vista', 'key': 'Windows NT 6.4'},
        {'name': 'Windows 7', 'key': 'Windows NT 6.4'},
        {'name': 'Windows xp', 'key': 'Windows NT 6.4'},
        {'name': 'Android', 'key': 'Android'},
        {'name': 'Linux', 'key': 'Linux'},
        {'name': 'iphone', 'key': 'iphone'},
        {'name': 'ipod', 'key': 'ipod'},
    ]
    for data in os_data:
        if re.search(data['key'], user_agent):
            return data['name']
    return "未知操作系统"
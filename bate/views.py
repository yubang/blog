# coding:UTF-8


from django.http import HttpResponse
from windPlug.core.browser import is_pc_browser, get_browser_type


def browser(request):
    """获取浏览器类型"""
    if is_pc_browser(request=request):
        m = "是电脑浏览器"
    else:
        m = "不是电脑浏览器"
    m = m + "\n" + get_browser_type(request)
    return HttpResponse(m)

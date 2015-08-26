# coding:UTF-8


"""
个人博客view
"""


from django.shortcuts import render_to_response


def index(request):
    """主页面"""
    return render_to_response("blog/index.html")
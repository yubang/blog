# coding:UTF-8


"""
个人博客view
"""


from django.shortcuts import render_to_response
from blog.models import BlogModel


def index(request):
    """主页面"""
    blogs = BlogModel.objects.order_by("-createTime").filter(status=0)
    return render_to_response("blog/index.html", {'blogs': blogs})


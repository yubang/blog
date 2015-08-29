# coding:UTF-8


"""
个人博客view
"""


from django.shortcuts import render_to_response
from blog.models import BlogModel


def index(request):
    """主页面"""

    page = int(request.GET.get('page', '1')) - 1
    if page < 0:
        page = 0
    next_page = page + 2
    last_page = page

    page_num = 10
    # 判断有没有下一页，并且获取总页数
    bllog_nums = BlogModel.objects.order_by("-createTime").filter(status=0).count()
    if bllog_nums <= (page + 1) * page_num:
        next_page = 0
    total_page = bllog_nums / page_num
    if bllog_nums % page_num:
        total_page += 1

    blogs = BlogModel.objects.order_by("-createTime").filter(status=0)[page*page_num:page*page_num+page_num]

    return render_to_response("blog/index.html", {'blogs': blogs, 'nextPage': next_page, 'lastPage': last_page, 'totalPage': range(1, total_page + 1), 'nowPage': page + 1})


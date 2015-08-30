# coding:UTF-8


"""
个人博客view
"""


from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.gzip import gzip_page
from blog.models import BlogModel, LabelModel


@gzip_page
def index(request):
    """主页面"""

    label = request.GET.get('type', None)
    key = request.GET.get('key', None)

    if key != None and label != None:
        url = "&type=%s&key=%s" % ((label, key))
    else:
        url = ""

    page = int(request.GET.get('page', '1')) - 1
    if page < 0:
        page = 0
    next_page = page + 2
    last_page = page

    page_num = 5
    # 判断有没有下一页，并且获取总页数
    if key == None and label == None:
        bllog_nums = BlogModel.objects.order_by("-createTime").filter(status=0).count()
    elif label == '':
        bllog_nums = BlogModel.objects.order_by("-createTime").filter(status=0, content__contains=key).count()
    else:
        bllog_nums = BlogModel.objects.order_by("-createTime").filter(status=0, label=label, content__contains=key).count()

    if bllog_nums <= (page + 1) * page_num:
        next_page = 0
    total_page = bllog_nums / page_num
    if bllog_nums % page_num:
        total_page += 1
    if not total_page:
        total_page = 1

    if key == None and label == None:
        blogs = BlogModel.objects.order_by("-createTime").filter(status=0)[page*page_num:page*page_num+page_num]
    elif label == '':
        blogs = BlogModel.objects.order_by("-createTime").filter(status=0, content__contains=key)[page*page_num:page*page_num+page_num]
    else:
        blogs = BlogModel.objects.order_by("-createTime").filter(status=0, label=label, content__contains=key)[page*page_num:page*page_num+page_num]

    #拉取所有标签
    labels = LabelModel.objects.filter(status=0)

    return render_to_response("blog/index.html", {'blogs': blogs, 'nextPage': next_page, 'lastPage': last_page, 'totalPage': range(1, total_page + 1), 'nowPage': page + 1, 'labels': labels, 'key': key, 'type': label, 'url': url, 'isAdmin': 'admin' in request.session})


def blog(request, blog_id):
    """显示博文"""
    try:
        blog = BlogModel.objects.get(id=blog_id, status=0)
        return render_to_response("blog/blog.html", {'blog': blog})
    except ObjectDoesNotExist:
        return HttpResponseNotFound("该博文不存在！")
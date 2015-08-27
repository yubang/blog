# coding:UTF-8


from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from blog.models import BlogModel, LabelModel
import datetime


def index(request):
    """主界面"""
    return render_to_response("admin/index.html")


def add_blog(request, blog_id):
    """添加博文"""
    if request.method == "GET":
        labels = LabelModel.objects.order_by("-createTime").filter(status__lt=2)
        obj = {}
        if blog_id != "0":
            obj = BlogModel.objects.get(id=blog_id)
        return render_to_response("admin/addBlog.html", {'obj': obj, 'labels': labels})
    else:
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        label = request.POST.get('label', None)
        obj = BlogModel(title=title, content=content, label=label, status=0, createTime=datetime.datetime.now())
        obj.save()
        return HttpResponseRedirect("/")

def add_label(request):
    """添加分类"""
    if request.method == "GET":
        labels = LabelModel.objects.order_by("-createTime").filter(status__lt=2)
        return render_to_response("admin/addLabel.html", {'labels': labels})
    else:
        content = request.POST.get('content', None)
        try:
            label = LabelModel(content=content, status=0, createTime=datetime.datetime.now())
            label.save()
        except IntegrityError:
            LabelModel.objects.filter(content=content, status=2).update(status=0, createTime=datetime.datetime.now())
        return HttpResponseRedirect("/admin/add/label")


def label_update(request, label_id, label_status):
    """更改标签状态"""
    LabelModel.objects.filter(id=label_id).update(status=label_status)
    return HttpResponseRedirect("/admin/add/label")
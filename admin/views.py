# coding:UTF-8


from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from blog.settings import ADMIN_PASSWORD, ADMIN_USER
from blog.models import BlogModel, LabelModel
from windPlug.script.migration import create_sql, migration_db
import datetime
import time


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

        if blog_id == "0":
            obj = BlogModel(title=title, content=content, label=label, status=0, createTime=datetime.datetime.now())
            obj.save()
        else:
            BlogModel.objects.filter(id=blog_id).update(title=title, content=content, label=label)

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


def delete_blog(request, blog_id):
    """删除博文"""
    BlogModel.objects.filter(id=blog_id).update(status=2)
    referer = request.META['HTTP_REFERER']
    return HttpResponseRedirect(referer)


def account(request):
    """后台管理员登录"""
    if request.method == "GET":
        return render_to_response("admin/account.html")
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if ADMIN_USER == username and ADMIN_PASSWORD == password:
            request.session['admin'] = time.time()
            return HttpResponseRedirect("/admin")
        else:
            return HttpResponseRedirect("/admin/account")


def migration(request, option):
    """
    同步数据库
    :param request: django的request对象
    :param option: 操作类型
    :return: HttpResponse
    """

    if option == "create":
        m = "创建的sql在：" + create_sql("data/sql")
    elif option == "migration":
        count = migration_db("data/sql")
        m = "执行的sql数：" + str(count)
    else:
        m = "fail"
    return HttpResponse(m)
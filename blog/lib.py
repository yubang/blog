# coding:UTF-8


from qiniu import Auth, put_data
from blog import settings
from django.http import HttpResponse, HttpResponseRedirect
import re
import json
import hashlib


def upload_image(request):
    """处理图片上传"""
    result = {"state": 'SUCCESS', "url": "", "title": '', "original": '', "type": '', "size": '',}

    data = request.FILES['upfile'].read()
    file_name = hashlib.md5(data).hexdigest()
    upload_file(file_name, data)

    result['url'] = "/pic/" + file_name

    response = HttpResponse(json.dumps(result))
    response['Content-Type'] = "application/json"
    return response


def ueditor(request):
    """处理ueditor"""
    action = request.GET.get('action')
    if action == 'config':
        data = open('static/ueditor/php/config.json', 'r').read()
        data = re.sub(r'\/\*[\s\S]+?\*\/', '', data)
        return HttpResponse(data)
    elif action == "uploadimage":
        #处理图片上传
        return upload_image(request)


def show_pic(request, pic_name):
    url = get_download_file_url(pic_name)
    return HttpResponseRedirect(url)


def upload_file(file_name, data):
    q = Auth(settings.QINIU_KEY, settings.QINIU_TOKEN)
    token = q.upload_token(settings.QINIU_BUCKET)
    ret, info = put_data(token, file_name, data)
    return ret['key'] == file_name


def get_download_file_url(file_name):
    """获取文件url"""
    q = Auth(settings.QINIU_KEY, settings.QINIU_TOKEN)
    base_url = 'http://%s/%s' % (settings.QINIU_HOST, file_name)
    private_url = q.private_download_url(base_url, expires=3600)
    return private_url

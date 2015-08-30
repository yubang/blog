# coding:UTF-8


from django.http import HttpResponseRedirect
import re


class AdminCheck(object):
    """管理员检查"""
    def process_request(self, request):
        if re.search(r'^/admin/', request.path) and request.path != '/admin/account' and 'admin' not in request.session:
            return HttpResponseRedirect("/admin/account")
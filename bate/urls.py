# coding:UTF-8

from django.conf.urls import url, patterns


urlpatterns = patterns('bate.views',
    url('^browser$', 'browser'),
)

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'blog.views.index'),
    url(r'^search$', 'blog.views.index'),
    url(r'^blog/(?P<blog_id>\d+)$', 'blog.views.blog'),
    url(r'^admin/', include('admin.urls')),

    url(r'^ueditor$', 'blog.lib.ueditor'),
    url(r'^pic/(?P<pic_name>.+)$', 'blog.lib.show_pic')
)

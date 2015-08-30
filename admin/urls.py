# coding:UTF-8


from django.conf.urls import url, patterns


urlpatterns = patterns('admin.views',
    url(r'^$', 'index'),
    url(r'^add/blog/(?P<blog_id>\d+)$', 'add_blog'),
    url(r'^add/label$', 'add_label'),
    url(r'^label/(?P<label_id>\d+)/(?P<label_status>\d+)$', 'label_update'),
    url(r'^deleteBlog/(?P<blog_id>\d+)$', 'delete_blog'),
)
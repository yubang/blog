# coding:UTF-8

from django.db import models


class BlogModel(models.Model):
    """博文模型"""
    title = models.CharField(max_length=100)
    content = models.TextField()
    status = models.SmallIntegerField()
    label = models.CharField(max_length=100)
    createTime = models.DateTimeField()

    class Meta:
        db_table = "blog_blog"


class LabelModel(models.Model):
    """博客标签模型"""
    content = models.CharField(max_length=10)
    status = models.SmallIntegerField()
    createTime = models.DateTimeField()

    class Meta:
        db_table = "blog_label"



# coding:UTF-8
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, editable=False)
    updated = models.DateTimeField(verbose_name=u'更新时间', auto_now=True, editable=False)
    ordering = models.IntegerField(verbose_name='排序', default=0)

    class Meta:
        abstract = True
        ordering = ['-ordering', '-id']
        verbose_name = u'基础模型'
        verbose_name_plural = verbose_name

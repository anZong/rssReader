# coding:UTF-8
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)

    class Meta:
        verbose_name = u'基础模型'
        verbose_name_plural = verbose_name

# coding:UTF-8
from django.db import models
from base.models import BaseModel


class User(BaseModel):
    username = models.TextField(verbose_name=u'用户名', max_length=32, unique=True, editable=False, blank=True, null=True)
    password = models.TextField(verbose_name=u'密码', max_length=128, blank=True, null=True)
    nickname = models.TextField(verbose_name=u'昵称', max_length=32, default='')
    phone = models.TextField(verbose_name=u'手机号码', max_length=11, blank=False, null=False)
    email = models.EmailField(verbose_name=u'邮箱', max_length=32, blank=True, null=True)
    openid = models.TextField(verbose_name=u'微信openid', default='')

    class Meta:
        ordering = ['id']
        verbose_name = u'用户'
        verbose_name_plural = verbose_name


class RssUrls(BaseModel):
    owner = models.ForeignKey(to=User, verbose_name=u'所属用户', on_delete=models.CASCADE, null=False, blank=False)
    title = models.TextField(verbose_name=u'标题', null=False, blank=False)
    url = models.URLField(verbose_name=u'链接地址', null=False, blank=False)

    class Meta:
        ordering = ['id']
        verbose_name = u'Rss地址'
        verbose_name_plural = verbose_name

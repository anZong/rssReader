# coding:UTF-8
from django.db import models

from base.models import BaseModel
from base.utils import obj2dic


class User(BaseModel):
    username = models.TextField(verbose_name=u'用户名', max_length=32, unique=True, editable=False, blank=True, null=True)
    password = models.TextField(verbose_name=u'密码', max_length=128, blank=True, null=True)
    nickname = models.TextField(verbose_name=u'昵称', max_length=32, default='')
    phone = models.TextField(verbose_name=u'手机号码', max_length=11, blank=True, null=True)
    email = models.EmailField(verbose_name=u'邮箱', max_length=32, blank=True, null=True)
    openid = models.TextField(verbose_name=u'微信openid', default='')
    avatar = models.TextField(verbose_name='头像', default='')
    gender = models.IntegerField(verbose_name=u'性别', choices=((0, '未知'), (1, '男'), (2, '女')), default=1)
    country = models.TextField(verbose_name='国家', default='')
    province = models.TextField(verbose_name='省份', default='')
    city = models.TextField(verbose_name='城市', default='')
    age = models.IntegerField(verbose_name='年龄', default=18)

    def to_json(self):
        return obj2dic(self, ['id', 'created'], {})

    def to_simple_json(self):
        return obj2dic(self, ['id'], {})

    class Meta:
        ordering = ['id']
        verbose_name = u'用户'
        verbose_name_plural = verbose_name
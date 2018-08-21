# coding:UTF-8
from django.db import models
from base.models import BaseModel

from base.utils import obj2dic, dic2obj


class Feed(BaseModel):
    title = models.TextField(verbose_name=u'标题', null=False, blank=False)
    subtitle = models.TextField(verbose_name=u'子标题', null=True, blank=True)
    url = models.URLField(verbose_name=u'链接地址', null=False, blank=False)

    def to_json(self):
        return obj2dic(self, ['id', 'title', 'subtitle', 'url'], {})

    class Meta:
        ordering = ['id']
        verbose_name = 'Rss地址'
        verbose_name_plural = verbose_name


class Feed2User(BaseModel):
    owner_user = models.ForeignKey(to='user.User', verbose_name=u'所属用户', on_delete=models.CASCADE, null=False, blank=False, related_name='rss2user_user')
    owner_feed = models.ForeignKey(to='feed.Feed', verbose_name=u'Rss', on_delete=models.CASCADE, null=False, blank=False, related_name='rss2user_feed')

    class Meta:
        verbose_name = '用户Rss'
        verbose_name_plural = verbose_name


class Post(BaseModel):
    owner_feed = models.ForeignKey(to='feed.Feed', verbose_name='所属Rss', on_delete=models.CASCADE, null=False, blank=False, related_name='post_feed')
    title = models.TextField(verbose_name='标题', default='')
    published = models.TextField(verbose_name='发布时间', default='')
    author = models.CharField(verbose_name='作者', default='', max_length=32)
    link = models.TextField(verbose_name='链接', default='')
    summary = models.TextField(verbose_name='描述', default='')
    content = models.TextField(verbose_name='内容', default='')

    @classmethod
    def create_by_entries(cls, feed_id, entries):
        res = []
        for entry in entries:
            post = cls.objects.filter(owner_feed_id=feed_id, title=entry.get('title')).first()
            if not post:
                post = cls.objects.create(owner_feed_id=feed_id)
            dic2obj(entry, ['title', 'published', 'author', 'link', 'summary', 'content'], post)
            post.save()
            res.append(post.to_json())
        return res

    def to_json(self):
        return obj2dic(self, ['id', 'title', 'published', 'author', 'link', 'summary', 'content'], {})

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

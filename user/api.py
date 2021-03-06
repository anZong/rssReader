# coding:UTF-8
import json
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from base.api import ApiView, asapi
from base.utils import dic2obj, py3get, gen_pager_array
from feed.utils import get_feed
from user.models import User
from feed.models import Feed, Feed2User, Post


def checklogin(self, request):
    if not self.get_me():
        raise Exception('用户未登录')


logined = asapi(login=True, checker=checklogin)
unlogin = asapi(login=False)


class UserApiView(ApiView):

    @unlogin
    def register(self, params, username, password):
        user = User.objects.filter(username=username)
        if user:
            raise Exception('用户名已被占用')
        user = User.objects.create()
        dic2obj(params, ['username', 'password', 'nickname', 'phone', 'gender', 'email', 'openid', 'city', 'age'], user)
        user.save()
        return {
            'username': username,
            'id': user.id
        }

    @unlogin
    def login(self, username, password):
        user = User.objects.filter(username=username, password=password).first()
        if not user:
            raise Exception('不存在该用户')
        self.session_set('me', user.to_simple_json())
        self.get_session().save()
        return {
            'msg': '登录成功'
        }

    @logined
    def logout(self):
        self.session_del('me')
        return {
            'msg': '退出成功'
        }

    @unlogin
    def wxa_login(self, params, appid, appsecret, code):
        wxserver = 'https://api.weixin.qq.com/sns/jscode2session'
        params = {
            'appid': appid,
            'secret': appsecret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        try:
            res = py3get(wxserver, params)
        except Exception as e:
            raise e
        res = json.loads(res)
        openid = res.get('openid')
        user = User.objects.filter(openid=openid).first()
        if not user:
            user = User.objects.create()
            dic2obj(params, ['username', 'phone', 'nickname', 'avatar', 'gender', 'country', 'province', 'city'], user)
            user.openid = openid
            user.save()

        self.session_set('me', user.to_simple_json())
        session = self.get_session()
        session.save()
        ids = Feed2User.objects.filter(owner_user_id=user.id).values_list('owner_feed_id', flat=True)
        feeds = Feed.objects.filter(id__in=ids)
        return {
            'sessionid': session.session_key,
            'feeds': gen_pager_array(feeds, {})
        }

    @logined
    def add_rss(self, params, url):
        feed = Feed.objects.filter(url=url).first()
        if feed:
            f2u = Feed2User.objects.filter(owner_feed=feed, owner_user_id=self.get_meid()).first()
            if f2u:
                raise Exception('订阅地址已添加')
        else:
            feed = Feed(url=url)
            feed_data = get_feed(url)
            dic2obj(feed_data, ['title', 'subtitle'], feed)
            feed.save()
            Post.create_by_entries(feed.id, feed_data.get('entries'))
        Feed2User.objects.create(owner_user_id=self.get_meid(), owner_feed=feed)
        return {
            'id': feed.id,
            'title': feed.title,
            'subtitle': feed.subtitle,
            'url': url,
        }

    @logined
    def search_rss(self, params, kw):
        query = Feed.objects.filter(title__icontains=kw)
        return gen_pager_array(query, params)

    @logined
    def refresh_posts(self, params, feed_id):
        feed = Feed.objects.filter(id=feed_id).first()
        feed_data = get_feed(feed.url)
        res = Post.create_by_entries(feed.id, feed_data.get('entries'))
        return res

    @logined
    def feed_list(self, params):
        ids = Feed2User.objects.filter(owner_user_id=self.get_meid()).values_list('owner_feed_id', flat=True)
        rss = Feed.objects.filter(id__in=ids)
        return gen_pager_array(rss, params)

    @logined
    def posts(self, params, feed_id):
        res = Post.objects.filter(owner_feed_id=feed_id).order_by('-published')
        return {
            'posts': gen_pager_array(query=res, params=params)
        }

    @logined
    def post(self, params, post_id):
        post = Post.objects.filter(id=post_id).first()
        if not post:
            raise Exception('不存在该文章')
        return {
            'post': post.to_detail_json()
        }

    @unlogin
    def parse_rss(self, url):
        res = get_feed(url)
        return res.get('rawdata')


urlpatterns = [
    path('<apiname>', csrf_exempt(UserApiView.as_view()))
]

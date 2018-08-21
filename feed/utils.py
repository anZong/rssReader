# coding:UTF-8
import feedparser
from base.utils import dict_assign


def gen_post(enty):
    res = dict_assign({}, ['title', 'link', 'author'], enty)
    pub = enty.get('published_parsed')
    res['published'] = '%s-%s-%s %s:%s:%s' % (pub[0], pub[1], pub[2], pub[3], pub[4], pub[5])
    res['summary'] = enty.get('summary')[:300]
    content = enty.get('content')[0]
    res['content'] = content and content.get('value', '')
    return res


def get_feed(url):
    try:
        res = feedparser.parse(url)
    except Exception as e:
        raise e
    posts = map(gen_post, res.entries)
    return {
        'title': res.feed.title,
        'subtitle': res.feed.subtitle,
        'entries': [post for post in posts]
    }

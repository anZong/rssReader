# coding:UTF-8
from datetime import date, datetime
import json, requests


def dict_assign(d1, k, d2):
    '''
    set d1 value from d2
    :param d1:{a:1,b:2}
    :param k: ['a','b'] or []
    :param d2: {a:2,b:5,c:3}
    :return: {a:2,b:5}
    '''
    keys = k or d1
    for key in keys:
        if key in d2:
            d1[key] = d2[key]
    return d1


def dic2obj(d, k, o):
    for key in k:
        if key in d:
            setattr(o, key, d[key])
    return o


def obj2dic(o, k, d):
    for key in k:
        if hasattr(o, key):
            d[key] = getattr(o, key)
    return d


def gen_pager_array(query, params, trans=None):
    page = int(params.get('page', 1))
    size = int(params.get('size', 10))
    start = (page - 1) * size
    end = page * size - 1
    query = query[start:end]
    return [trans(item) if trans else item.to_json() for item in query]


def py3get(url, data):
    res = requests.get(url, data)
    return res.text


def py3post(url, data):
    res = requests.post(url, data)
    return res.text


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                'timestamp': int(obj.timestamp()),
                'datetime': obj.strftime('%Y-%m-%d %H:%M%S')
            }
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)

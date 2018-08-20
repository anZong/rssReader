# coding:UTF-8
from django.http import HttpResponse
import inspect
from base.views import BaseView


class ApiView(BaseView):
    def get(self, request, apiname):
        func = getattr(self, apiname)
        if not func:
            raise Exception(u'不存在该接口')
        params = {}
        if request.GET:
            params.update(dict(request.GET.items()))
        if request.POST:
            params.update(dict(request.POST.items()))
        try:
            _res = func(**params)
            res = {
                'code':0,
                'data': _res,
            }
        except Exception as e:
            res = {
                'code': -1,
                'msg': e.args[0]
            }

        return self.parse_res(res)

    def parse_res(self, cxt):
        import json
        return HttpResponse(content=json.dumps(cxt),content_type='text/plain')

    def test(self, params):
        cxt = {
            'test': True
        }
        return cxt

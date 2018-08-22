# coding:UTF-8
from django.http import HttpResponse

from base.views import BaseView
from base.utils import dict_assign, JsonEncoder


class ApiView(BaseView):
    def get(self, request, apiname):
        apifunc = getattr(self, apiname)
        if not apifunc:
            raise Exception(u'不存在该接口')

        func_args = getattr(apifunc, 'func_args')
        needlogin = getattr(apifunc, 'login')
        checker = getattr(apifunc, 'checker')

        if needlogin and checker:
            checker(self, request)

        params = {}
        if request.GET:
            params.update(dict(request.GET.items()))
        if request.POST:
            params.update(dict(request.POST.items()))

        try:
            _params = dict_assign({}, func_args, params)
            if 'params' in func_args:
                _params['params'] = _params
            _res = apifunc(**_params)
            res = {
                'code': 0,
                'data': _res,
            }
        except Exception as e:
            res = {
                'code': -1,
                'msg': e.args[0] if e.args else 'error!'
            }

        return self.api_response(res)

    def api_response(self, cxt):
        import json
        if self.get_me():
            cxt['user'] = self.get_me()
        return HttpResponse(content=json.dumps(cxt, cls=JsonEncoder), content_type='text/plain')

    def test(self, params):
        cxt = {
            'test': True
        }
        return cxt


def asapi(login=True, checker=None):
    def _func(func):
        def __func(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        import inspect
        # 获取接口参数
        func_args = inspect.getfullargspec(func).args[1:]
        setattr(__func, 'func_args', func_args)
        setattr(__func, 'login', login)
        setattr(__func, 'checker', checker)
        return __func

    return _func

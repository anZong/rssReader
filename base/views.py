# coding:UTF-8
from django.views import View


class BaseView(View):

    def get_session(self):
        return self.request.session

    def session_set(self, key, val):
        self.get_session()[key] = val

    def session_get(self, key):
        if key in self.get_session():
            return self.get_session().get(key)

    def session_del(self, key):
        if key in self.get_session():
            del self.get_session()[key]

    def get_me(self):
        return self.session_get('me')

    def get_meid(self):
        me = self.get_me()
        return me and me.get('id') or None

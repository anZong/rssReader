# coding:UTF-8
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from base.api import ApiView
from user.models import User


class UserApiView(ApiView):

    def adduser(self, username, password):
        return {
            'username': username,
            'password': password
        }


urlpatterns = [
    path('<apiname>', csrf_exempt(UserApiView.as_view()))
]

# coding:UTF-8
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from base.api import ApiView


class AdminApiView(ApiView):
    pass


urlpatterns = [

]
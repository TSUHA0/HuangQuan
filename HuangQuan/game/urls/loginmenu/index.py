# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/4/28 17:49 
# @File:index.py

from django.http import JsonResponse
from django.urls import path


def index(request):
    response = {'msg': 'success'}
    return JsonResponse(response)


urlpatterns = [
    path("login", index, name="index")
]

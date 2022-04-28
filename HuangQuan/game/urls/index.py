# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/4/28 17:42 
# @File:index.py.py

from django.urls import path, include


urlpatterns = [
    path("api/", include("game.urls.loginmenu.index")),
]

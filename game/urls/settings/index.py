# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/5/1 18:05 
# @File:index.py

from django.urls import path
from game.views.settings.loginfo import getinfo
from game.views.settings.login import signin
from game.views.settings.logout import signout
from game.views.settings.register import register

urlpatterns = [
    path("getinfo/", getinfo, name="settings_getinfo"),
    path("login/", signin, name="settings_login"),
    path("logout/", signout, name="settings_logout"),
    path("register/", register, name="settings_register"),
]

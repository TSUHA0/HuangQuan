# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/5/1 13:26 
# @File:routing.py

from django.urls import path
from game.consumers.multiplayer.index import MultiPlayer

websocket_urlpatterns = [
    path("wss/multiplayer/", MultiPlayer.as_asgi(), name="wss_multiplayer"),
]

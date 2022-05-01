# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/5/1 11:33 
# @File:index.py
import asyncio

from channels.generic.websocket import WebsocketConsumer
import json
from django.conf import settings
from django.core.cache import cache


class MultiPlayer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.accept()

    def disconnect(self, close_code):
        print('disconnect')

    def websocket_receive(self, text_data):
        print(text_data)

# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/4/28 17:49 
# @File:index.py

from django.http import JsonResponse
from django.urls import path
import threading

class MyModel():
    _counter = 0
    _counter_lock = threading.Lock()

    @classmethod
    def increment_counter(cls):
        with cls._counter_lock:
            cls._counter += 1

    def some_action(self):
        # core code
        self.increment_counter()

    def get_cnt(self):
        return self._counter

def index(request):
    MyModel().some_action()
    response = {'msg': 'serv msg:' + str(MyModel().get_cnt())}
    return JsonResponse(response)


urlpatterns = [
    path("login", index, name="index")
]

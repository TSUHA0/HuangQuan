# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/5/1 18:09 
# @File:login.py

from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def signin(request):
    data = request.POST
    username = data.get('username')
    password = data.get('password')
    print(data)
    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({
            'result': "用户名或密码不正确"
        })
    login(request, user)
    return JsonResponse({
        'result': "success"
    })

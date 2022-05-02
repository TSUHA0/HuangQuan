# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/5/1 18:10 
# @File:logout.py

from django.http import JsonResponse
from django.contrib.auth import logout


def signout(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({
            'result': "success",
        })
    logout(request)
    return JsonResponse({
        'result': "success",
    })

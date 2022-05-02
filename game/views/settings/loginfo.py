# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/5/1 18:05 
# @File:loginfo.py

from django.http import JsonResponse
from game.models.player.player import Player


def getinfo_web(request):
    user = request.user
    print(user)
    if not user.is_authenticated:
        return JsonResponse({
            'result': "未登录"
        })
    else:
        player = Player.objects.get(user=user)
        return JsonResponse({
            'result': "success",
            'username': player.user.username,
            'photo': player.photo,
        })


def getinfo(request):
    return getinfo_web(request)

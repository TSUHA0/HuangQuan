# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/5/1 11:33 
# @File:index.py
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.conf import settings
from django.core.cache import cache


class MultiPlayer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.username = ""
        self.room_id = "0"
        self.room_owner = False

    async def connect(self):
        print('connect')
        await self.accept()

    async def disconnect(self, close_code):
        if self.username != "" and self.room_id != "0":
            players = cache.get(self.room_id)
            for player in players:
                if player['username'] == self.username:
                    players.remove(player)
                    break
            cache.set(self.room_id, players)
            print('disconnect')
            await self.channel_layer.group_send(
                self.room_id,
                {
                    'type': "group_player",
                    'event': "delete_player",
                    'username': self.username
                })
            await self.channel_layer.group_discard(self.room_id, self.channel_name);

    async def recover_game(self, data):
        players = cache.get(self.room_id)
        data = {
            'event': "recover_game",
            'players': players,
        }
        await self.send(text_data=json.dumps(data))

    async def create_player(self, data):
        players = cache.get(self.room_id)
        players.append({
            'username': data['username'],
        })

        for player in cache.get(self.room_id):
            await self.send(text_data=json.dumps({
                'event': "create_player",
                'username': player['username'],
            }))

        cache.set(self.room_id, players, 7200)
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_player",
                'event': "create_player",
                'username': data['username'],
            }
        )

    async def group_player(self, data):
        await self.send(text_data=json.dumps(data))

    async def join_room(self, data):
        if self.room_id not in cache:
            cache.set(self.room_id, [], 7200)  # 有效期2小时

        not_need_rec = True
        for player in cache.get(self.room_id):
            if player['username'] == data['username']:
                not_need_rec = False
                await self.recover_game(data)
        # 如果玩家 >8 这里要处理一下
        # todo

        if not_need_rec:
            await self.create_player(data)

    async def game_init(data):
        pass
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data['event']
        if event == "joinroom":
            self.username = data['username']
            self.room_id = data['roomid']
            await self.join_room(data)
        elif event == "gamestart":
            await self.game_init(data)

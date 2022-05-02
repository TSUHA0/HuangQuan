# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/5/1 11:33 
# @File:index.py
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.cache import cache
from HuangQuan.settings import CARD_NUM
from game.consumers.multiplayer.cardlist import init_card_list, init_behind_list, init_front_list, init_role_list


class MultiPlayer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.username = ""
        self.room_id = ""
        self.card_list_key = ""
        self.card_list_pos = ""

    def get_card_list_key(self):
        return "card_list" + self.room_id

    def get_card_list_pos_key(self):
        return "card_pos" + self.room_id

    def get_player_game_status_key(self, username):
        return username + self.room_id

    def get_room_satus_key(self):
        return "status" + self.room_id

    def draw_card(self):
        card_pos = cache.get(self.get_card_list_pos_key())
        # 暂时不考虑洗牌
        cache.set(self.get_card_list_pos_key(), (card_pos + 1) % CARD_NUM)
        return cache.get(self.get_card_list_key())[card_pos]

    async def connect(self):
        print('connect')
        await self.accept()

    async def disconnect(self, close_code):
        print('disconnect')
        players = cache.get(self.room_id)
        for player in players:
            if player['username'] == self.username:
                players.remove(player)
                await self.channel_layer.group_send(
                    self.room_id,
                    {
                        'type': "group_player",
                        'event': "delete_player",
                        'username': self.username
                    })
                await self.channel_layer.group_discard(self.room_id, self.channel_name)
        cache.set(self.room_id, players, 7200)

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
            cache.set(self.get_room_satus_key(), False)

        not_need_rec = True
        for player in cache.get(self.room_id):
            if player['username'] == data['username']:
                not_need_rec = False
                await self.recover_game(data)
        # 如果玩家 >8 这里要处理一下
        # todo
        if not_need_rec:
            await self.create_player(data)

    async def send_game_status(self, type):
        players = cache.get(self.room_id)
        game_status = []
        for player in players:
            game_status.append(cache.get(self.get_player_game_status_key(player['username'])))

        if type == "all":
            await self.channel_layer.group_send(
                self.room_id, {
                    'type': "group_player",
                    'event': "game_status",
                    'data': game_status,
                })
        elif type == "mono":
            await self.send(text_data=json.dumps(game_status))

    async def game_init(self):
        if cache.get(self.get_room_satus_key()):
            return await self.send(text_data=json.dumps({
                "status": "error",
                "result": "对局正在进行，请选择重新连接游戏"
            }))
        cache.set(self.get_room_satus_key(), True)
        card_list = init_card_list()
        cache.set(self.get_card_list_key(), card_list, 7200)
        cache.set(self.get_card_list_pos_key(), 0, 7200)
        players = cache.get(self.room_id)
        idx = 0
        players_num = len(players)
        behind_list = init_behind_list()
        front_list = init_front_list()
        role_list = init_role_list(players_num)
        if len(role_list) == 0:
            cache.set(self.get_room_satus_key(), False)
            return await self.send(text_data=json.dumps({
                "status": "error",
                "result": "人数不满足对局要求"
            }))
        for player in players:
            hand_card = []
            for i in range(4):
                hand_card.append(self.draw_card())
            behind = behind_list[idx]
            front = front_list[idx]
            role = role_list[idx]
            idx += 1
            cache.set(self.get_player_game_status_key(player['username']),
                      {
                          'username': player['username'],
                          'role': role,
                          'pos': idx,
                          'behind': behind,
                          'front': front,
                          'behind_status': False,
                          'hand_card': hand_card,
                          'blue': [],
                          'red': [],
                          'gray': [],
                          'deliver': 0,
                      })
        await self.send_game_status("all")

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data['event']
        if event == "joinroom":
            self.username = str(data['username'])
            self.room_id = str(data['roomid'])
            await self.join_room(data)
        elif event == "gamestart":
            await self.game_init()

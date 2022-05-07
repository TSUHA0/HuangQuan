# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/5/1 11:33 
# @File:index.py
import asyncio
import random

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.cache import cache
from HuangQuan.settings import CARD_NUM
from game.consumers.multiplayer.cardlist import init_card_list, init_behind_list, init_front_list, init_role_list
from game.consumers.multiplayer.secretcard import secretcard


def get_card_color(cardId):
    color = secretcard[int(cardId)]["color"]
    if color == "黑":
        return "gray"
    if color == "蓝":
        return "blue"
    if color == "红":
        return "red"
    return ""


def get_role(role):
    if role == 1:
        return "王道"
    if role == 2:
        return "霸道"
    if role == 3:
        return "心道"
    return ""


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
        cache.set(self.get_card_list_pos_key(), (1 + int(card_pos)) % CARD_NUM)
        return cache.get(self.get_card_list_key())[card_pos]

    async def draw_card_with_num(self, num):
        card_list = []
        for i in range(num):
            card_list.append(self.draw_card())
        player = cache.get(self.get_player_game_status_key(self.username))
        for card in card_list:
            player['hand_card'].append(card)
        cache.set(self.get_player_game_status_key(self.username), player)
        await self.channel_layer.group_send(
            self.room_id, {
                'type': "group_event_send",
                'event': "draw_card",
                'username': self.username,
                'card_list': card_list,
            })

    async def connect(self):
        print('connect')
        await self.accept()

    async def disconnect(self, close_code):
        print('disconnect')
        await self.channel_layer.group_discard(self.room_id, self.channel_name)
        if cache.get(self.get_room_satus_key()):
            return
        players = cache.get(self.room_id)
        if not players:
            return
        for player in players:
            if player['username'] == self.username:
                players.remove(player)
                await self.channel_layer.group_send(
                    self.room_id,
                    {
                        'type': "group_event_send",
                        'event': "delete_player",
                        'username': self.username
                    })
        cache.set(self.room_id, players, 7200)

    async def return_error(self, errmsg):
        return await self.send(text_data=json.dumps({
            "status": "error",
            "result": errmsg
        }))

    async def recover_game_room(self, data):
        players = cache.get(self.room_id)
        data = {
            'event': "recover_game",
            'players': players,
        }
        await self.send(text_data=json.dumps(data))
        await self.channel_layer.group_add(self.room_id, self.channel_name)

    async def recover_game_round(self):
        await self.send_game_status("mono")

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
                'type': "group_event_send",
                'event': "create_player",
                'username': data['username'],
            }
        )

    async def group_event_send(self, data):
        await self.send(text_data=json.dumps(data))

    async def join_room(self, data):
        if self.room_id not in cache:
            cache.set(self.room_id, [], 7200)  # 有效期2小时
            cache.set(self.get_room_satus_key(), False)

        not_need_rec = True
        for player in cache.get(self.room_id):
            if player['username'] == data['username']:
                not_need_rec = False
                await self.recover_game_room(data)
        # 如果玩家 >8 这里要处理一下
        # todo
        if not_need_rec and not cache.get(self.get_room_satus_key()):
            await self.create_player(data)

    async def send_game_status(self, type):
        players = cache.get(self.room_id)
        game_status = []
        for player in players:
            game_status.append(cache.get(self.get_player_game_status_key(player['username'])))

        if type == "all":
            await self.channel_layer.group_send(
                self.room_id, {
                    'type': "group_event_send",
                    'event': "game_status",
                    'data': game_status,
                })
        elif type == "mono":
            await self.send(text_data=json.dumps({
                'event': "game_status",
                'data': game_status,
            }))

    async def game_init(self):
        if cache.get(self.get_room_satus_key()):
            players = cache.get(self.room_id)
            for player in players:
                if player['username'] == self.username:
                    return await self.recover_game_round()
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
        random_n = random.randint(1, players_num)
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
            is_chief = False
            if idx == random_n:
                is_chief = True
            cache.set(self.get_player_game_status_key(player['username']),
                      {
                          'username': player['username'],
                          'role': get_role(role),
                          'pos': idx,
                          'behind': behind,
                          'front': front,
                          'witch_status': 'front',
                          'is_chief': is_chief,
                          'round_owner': False,
                          'hand_card': hand_card,
                          'blue': [],
                          'red': [],
                          'gray': [],
                          'deliver': 0,
                      })
        await self.send_game_status("all")

    async def hand_to_receive(self, data):
        player = cache.get(self.get_player_game_status_key(data['target']))
        id = data['cardid']
        color = get_card_color(id)
        if color == "":
            return await self.return_error("卡牌ID有误，颜色不对")
        player[color].append(id)
        cache.set(self.get_player_game_status_key(data['target']), player)
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                "event": "hand_to_receive",
                "username": data['username'],
                "target": data['target'],
                'blue': player['blue'],
                'red': player['red'],
                'gray': player['gray'],
                "update_msg": data['update_msg']
            }
        )

    async def play_card(self, data):
        player = cache.get(self.get_player_game_status_key(self.username))
        for card in player['hand_card']:
            if card == data['cardid']:
                player['hand_card'].remove(card)
        cache.set(self.get_player_game_status_key(self.username), player)
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                'event': "play_card",
                'username': self.username,
                'cardid': data['cardid'],
                'update_msg': data['update_msg']
            }
        )

    async def secret_play_card(self, data):
        player = cache.get(self.get_player_game_status_key(self.username))
        for card in player['hand_card']:
            if card == data['cardid']:
                player['hand_card'].remove(card)
        cache.set(self.get_player_game_status_key(self.username), player)
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                'event': "secret_play_card",
                'username': self.username,
                'target': data['target'],
                'cardid': data['cardid'],
            }
        )

    async def deliver_card(self, data):
        player = cache.get(self.get_player_game_status_key(self.username))
        id = data['cardid']
        player['deliver'] = id
        if id in player['hand_card']:
            player['hand_card'].remove(id)
        cache.set(self.get_player_game_status_key(self.username), player)
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                'event': "deliver_card",
                'username': self.username,
                'cardid': id
            }
        )

    async def accept_deliver(self, data):
        player = cache.get(self.get_player_game_status_key(self.username))
        id = data['cardid']
        color = get_card_color(id)
        if color == "":
            return await self.return_error("卡牌ID有误，颜色不对")
        player[color].append(id)
        cache.set(self.get_player_game_status_key(self.username), player)
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                'event': "accept_deliver",
                'username': self.username,
                'color': secretcard[id]["color"],
                'blue': player['blue'],
                'red': player['red'],
                'gray': player['gray'],
            }
        )

    async def behind_come(self, data):
        player = cache.get(self.get_player_game_status_key(self.username))
        player['witch_status'] = 'behind'
        cache.set(self.get_player_game_status_key(self.username), player)
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                'event': "behind_come",
                'username': self.username,
            }
        )

    async def show_role_info(self, data):
        player = cache.get(self.get_player_game_status_key(data['target']))
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                'event': "show_role_info",
                'username': self.username,
                "target": data['target'],
                "role": player['role']
            }
        )

    async def hand_to_hand(self, data):
        me = cache.get(self.get_player_game_status_key(self.username))
        player = cache.get(self.get_player_game_status_key(data['target']))
        n = random.randint(0, len(player['hand_card']) - 1)
        id = player['hand_card'][n]
        me['hand_card'].append(id)
        player['hand_card'].remove(id)
        cache.set(self.get_player_game_status_key(self.username), me)
        cache.set(self.get_player_game_status_key(data['target']), player)

        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                'event': "hand_to_hand",
                'username': self.username,
                "target": data['target'],
                "me_card_list": me['hand_card'],
                "target_card_list": player['hand_card'],
                "update_msg": data['update_msg']
            }
        )

    async def hand_replace_deliver(self, data):
        players = cache.get(self.room_id)
        for name in players:
            player = cache.get(self.get_player_game_status_key(name['username']))
            if player['deliver'] != 0:
                player['deliver'] = data['cardid']
                cache.set(self.get_player_game_status_key(player['username']), player)
                await self.channel_layer.group_send(
                    self.room_id,
                    {
                        'type': "group_event_send",
                        'event': "hand_replace_deliver",
                        'username': self.username,
                        'cardid': data['cardid'],
                        'update_msg': data['update_msg']
                    }
                )

    async def update_action_log(self, data):
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                'event': "update_action_log",
                'update_msg': data['update_msg']
            }
        )

    async def reverse_deliver(self, data):
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                'event': "reverse_deliver",
                'update_msg': data['update_msg']
            }
        )

    async def drop_receive(self, data):
        player = cache.get(self.get_player_game_status_key(data['target']))
        id = int(data['cardid'])
        color = get_card_color(id)
        if color == "":
            return await self.return_error("卡牌ID有误，颜色不对")
        if id in player[color]:
            player[color].remove(id)
        cache.set(self.get_player_game_status_key(data['target']), player)
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                "event": "drop_receive",
                "target": data['target'],
                'blue': player['blue'],
                'red': player['red'],
                'gray': player['gray'],
                "update_msg": data['update_msg']
            }
        )

    async def receive_to_hand(self, data):
        player = cache.get(self.get_player_game_status_key(data['target']))
        id = int(data['cardid'])
        color = get_card_color(id)
        if color == "":
            return await self.return_error("卡牌ID有误，颜色不对")
        if id in player[color]:
            player[color].remove(id)
        cache.set(self.get_player_game_status_key(data['target']), player)

        me = cache.get(self.get_player_game_status_key(self.username))
        me['hand_card'].append(id)
        cache.set(self.get_player_game_status_key(self.username), me)
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                "event": "receive_to_hand",
                "username": self.username,
                "cardid": id,
                "target": data['target'],
                'blue': player['blue'],
                'red': player['red'],
                'gray': player['gray'],
                "update_msg": data['update_msg']
            }
        )

    async def receive_to_receive(self, data):
        player = cache.get(self.get_player_game_status_key(data['target']))
        id = int(data['cardid'])
        color = get_card_color(id)
        if color == "":
            return await self.return_error("卡牌ID有误，颜色不对")
        if id in player[color]:
            player[color].remove(id)
        cache.set(self.get_player_game_status_key(data['target']), player)

        me = cache.get(self.get_player_game_status_key(self.username))
        me[color].append(id)
        cache.set(self.get_player_game_status_key(self.username), me)
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                "event": "hand_to_receive",
                "target": data['target'],
                'blue': player['blue'],
                'red': player['red'],
                'gray': player['gray'],
                "update_msg": data['update_msg']
            }
        )
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': "group_event_send",
                "event": "hand_to_receive",
                "target": self.username,
                'blue': me['blue'],
                'red': me['red'],
                'gray': me['gray'],
                "update_msg": ""
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data['event']
        if event == "join_room":
            self.username = str(data['username'])
            self.room_id = str(data['roomid'])
            await self.join_room(data)
        elif event == "game_start":
            await self.game_init()
        elif event == "draw_card":
            await self.draw_card_with_num(data['cardnum'])
        elif event == "play_card":
            await self.play_card(data)
        elif event == "secret_play_card":
            await self.secret_play_card(data)
        elif event == "deliver_card":
            await self.deliver_card(data)
        elif event == "accept_deliver":
            await self.accept_deliver(data)
        elif event == "behind_come":
            await self.behind_come(data)
        elif event == "hand_to_receive":
            await self.hand_to_receive(data)
        elif event == "show_role_info":
            await self.show_role_info(data)
        elif event == "hand_to_hand":
            await self.hand_to_hand(data)
        elif event == "hand_replace_deliver":
            await self.hand_replace_deliver(data)
        elif event == "update_action_log":
            await self.update_action_log(data)
        elif event == "reverse_deliver":
            await self.reverse_deliver(data)
        elif event == "drop_receive":
            await self.drop_receive(data)
        elif event == "receive_to_hand":
            await self.receive_to_hand(data)
        elif event == "receive_to_receive":
            await self.receive_to_receive(data)

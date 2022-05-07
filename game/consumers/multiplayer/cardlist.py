# Author:Tsuhao
# -*- coding=utf-8 -*- 
# @Time:2022/5/2 17:24 
# @File:cardlist.py
import time
import random
from HuangQuan.settings import FRONT_ROLE_NUM, BEHIND_ROLE_NUM


def get_random_list(start, stop, n):
    '''
    生成范围在[start,stop], 长度为n的数组.
    区间包含左右endpoint
    '''
    arr = list(range(start, stop + 1))
    shuffle_n(arr, n)
    return arr[-n:]


def shuffle_n(arr, n):
    random.seed(time.time())
    for i in range(len(arr) - 1, len(arr) - n - 1, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]


def init_front_list():
    return get_random_list(1, FRONT_ROLE_NUM, FRONT_ROLE_NUM)


def init_behind_list():
    return get_random_list(1, BEHIND_ROLE_NUM, BEHIND_ROLE_NUM)


def init_card_list():
    return get_random_list(1, 92, 92)


def init_role_list(n):
    ret = []
    if n == 6:
        ret = [1, 1, 2, 2, 3, 3]
        shuffle_n(ret, 6)
    elif n == 5:
        ret = [1, 1, 2, 2, 3]
        shuffle_n(ret, 5)
    elif n == 4:
        ret = [1, 1, 2, 2]
        shuffle_n(ret, 4)
    elif n == 3:
        ret = [1, 2, 3]
    return ret

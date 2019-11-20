#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/9 0009 14:06
# @Author : Zhaozhen
# @File : __init__.py.py
# @Software: PyCharm

import time
import socket
import json
import struct
sk = socket.socket()

def my_recv(sk):
    pack_len = sk.recv(4)
    len_msg = struct.unpack('i', pack_len)[0]
    msg = sk.recv(len_msg).decode('utf-8')
    msg_b = json.loads(msg)
    return msg_b

sk.connect(('127.0.0.1',9002))
for i in range(100000):i*2
msg = my_recv(sk)
print(msg)
msg = my_recv(sk)
print(msg)
sk.close()
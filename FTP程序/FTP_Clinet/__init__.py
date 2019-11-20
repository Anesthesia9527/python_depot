#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/9 0009 13:51
# @Author : Zhaozhen
# @File : __init__.py.py
# @Software: PyCharm

import socket
import struct
import json

def my_send(conn,msg):
    msg_b = json.dumps(msg).encode('utf-8')
    len_msg = len(msg_b)
    pack_len = struct.pack('i', len_msg)
    conn.send(pack_len)
    conn.send(msg_b)

sk = socket.socket()
sk.bind(('127.0.0.1',9002))
sk.listen()

conn,addr = sk.accept()
msg1 = '你好'
msg2 = '吃了么'
my_send(conn,msg1)
my_send(conn,msg2)
conn.close()
sk.close()
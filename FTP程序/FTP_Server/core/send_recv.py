#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/14 0014 21:44
# @Author : Zhaozhen
# @File : send_recv.py
# @Software: PyCharm

import json
import struct
from core import log

class SendAndRecv:
    # 向client发送内容
    @staticmethod
    def mysend(request,dic):
        str_d = json.dumps(dic)
        request.send(str_d.encode('utf-8'))

    # 接受client发送的内容
    @staticmethod
    def myrecv(request):
        bytes_len = request.recv(4)
        msg_len = struct.unpack('i', bytes_len)[0]
        msg = request.recv(msg_len).decode('utf-8')
        opt_dic = json.loads(msg)
        return opt_dic
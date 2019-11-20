#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/9 0009 15:17
# @Author : Zhaozhen
# @File : send_receive.py
# @Software: PyCharm

import json
import struct
import os
import hashlib

class SendAndRecv:

    # 接受server发送过来的值并做处理
    @staticmethod
    def send_dic(sk,dic):
        bytes_d = json.dumps(dic).encode('utf-8')
        len_b = len(bytes_d)
        len_dic = struct.pack('i',len_b)
        sk.send(len_dic)
        sk.send(bytes_d)
    # 向server端发送至
    @staticmethod
    def recv_dic(sk):
        str_dic = sk.recv(1024).decode('utf-8')
        ret_dic = json.loads(str_dic)
        return ret_dic

    # 获取未下载完成文件的字节大小
    @staticmethod
    def get_md5(file):
        if os.path.exists(file):
            md5 = hashlib.md5()
            with open(file, 'rb') as f:
                str = f.read()
                md5.update(str)
            file_md5 = md5.hexdigest()
            return file_md5


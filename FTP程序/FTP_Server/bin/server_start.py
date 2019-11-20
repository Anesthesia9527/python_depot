#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/9 0009 13:50
# @Author : Zhaozhen
# @File : server_start.py
# @Software: PyCharm

import os,sys
import socketserver

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_PATH)

from core.user_auth import Auth
from core.send_recv import SendAndRecv
from core.ftp_server import FilePutGet

class Myserver(socketserver.BaseRequestHandler,SendAndRecv):

    def handle(self):
        while True:
            # 接受client发送过来的内容
            opt_dic = self.myrecv(self.request)
            # 用户登录，注册操作
            if opt_dic:
                # 判断有此操作
                if hasattr(Auth,opt_dic['operate']):
                    # 调用此操作获取返回值
                    dic = getattr(Auth,opt_dic['operate'])(opt_dic)
                    # 如果返回值是quit就结束此客户端连接
                    if dic['operate'] == 'quit':
                        self.mysend(self.request,dic)
                        break
                    self.mysend(self.request,dic)
            # 文件操作，判断有此操作
            if hasattr(FilePutGet,opt_dic['operate']):
                # 调用此操作
                getattr(FilePutGet,opt_dic['operate'])(self.request,opt_dic)
        # 结束此连接
        self.request.close()


if __name__ == '__main__':
    sk = socketserver.ThreadingTCPServer(('127.0.0.1',9050),Myserver)
    sk.serve_forever()

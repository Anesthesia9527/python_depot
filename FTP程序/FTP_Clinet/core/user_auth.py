#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/14 0014 21:46
# @Author : Zhaozhen
# @File : user_auth.py
# @Software: PyCharm

import json
import os
from core.send_recv import SendAndRecv
from conf.settings import *

class UserOperation:

    # 获取登录用户
    User = None
    # 获取用户的家目录
    User_path = None
    # 获取用户所在的目录
    Home_path = None

    @staticmethod
    def obtain_user(operation='login'):
        user,pwd = input("请输入用户名：").strip(),input("请输入用户密码：").strip()
        # 判断是注册
        if user and pwd and operation == 'register':
            # 二次密码
            pwd2 = input("请在次输入密码确认：").strip()
            # 判断两次密码输入是否正确
            if pwd == pwd2:
                dic = {'username':user,'password':pwd,'operate':operation}
                return dic
        # 判断是登录
        elif user and pwd:
            dic = {'username':user,'password':pwd,'operate':operation}
            return dic
    # 登录函数功能
    @classmethod
    def login(cls,sk):
        print("\033[1;31;46m用户登录页面\033[0m".center(34, "#"))
        dic = cls.obtain_user()
        if dic:SendAndRecv.send_dic(sk,dic)
        ret_dic = SendAndRecv.recv_dic(sk)
        if ret_dic['operate'] == 'login' and ret_dic['flag']:
            # 保存当前登录用户,后续调用
            cls.User = ret_dic['username']
            # 获取所有用户的目录
            cls.Home_path = os.path.join(DB,'Home')
            # 获取登录用户的家目录
            cls.User_path = os.path.join(cls.Home_path,ret_dic['username'])
            print("用户：{}.登录成功".format(ret_dic['username']))
            return (ret_dic['operate'],ret_dic['flag'])
        else:
            print("用户：{}.登录失败".format(ret_dic['username']))
    # 注册函数功能
    @classmethod
    def register(cls,sk):
        print("\033[1;31;46m用户注册页面\033[0m".center(34, "#"))
        dic = cls.obtain_user('register')
        if dic:SendAndRecv.send_dic(sk,dic)
        ret_dic = SendAndRecv.recv_dic(sk)
        if ret_dic['operate'] == 'register' and ret_dic['flag']:
            # 获取所有用户的目录
            cls.Home_path = os.path.join(DB,'Home')
            # 获取注册用户的家目录
            cls.User_path = os.path.join(cls.Home_path,ret_dic['username'])
            # 判断Home目录不存在创建
            if not os.path.exists(cls.Home_path):os.mkdir(cls.Home_path)
            # 判断用户目录不存在创建
            if not os.path.exists(cls.User_path):os.mkdir(cls.User_path)
            print("用户：{}.注册成功".format(ret_dic['username']))
        else:
            print("用户：{}.注册失败".format(ret_dic['username']))
    # 退出程序功能函数
    @staticmethod
    def quit(sk):
        dic = {'operate':'quit','tag':'Q'}
        SendAndRecv.send_dic(sk,dic)
        ret_dic = SendAndRecv.recv_dic(sk)
        if ret_dic['flag']:
            exit()
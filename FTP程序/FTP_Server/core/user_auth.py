#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/11 0011 22:23
# @Author : Zhaozhen
# @File : user_auth.py
# @Software: PyCharm

import hashlib
import os

from conf.settings import *
from core import log

class Auth:

    # 获取当前登录用户
    User = None
    # 获取登录用户所在的目录
    Home_path = None
    # 获取登录用户的家目录
    User_path = None

    # 获取用户密码的MD5值
    @staticmethod
    def get_md5(opt_dic):
        md5 = hashlib.md5(opt_dic['username'].encode('utf-8'))
        md5.update(opt_dic['password'].encode('utf-8'))
        pwd = md5.hexdigest()
        return pwd

    # 读取用户文件,用户注册时,判断
    @staticmethod
    def read_user(path):
        with open(path,mode='r',encoding='utf-8') as f:
            for name_lst in f:
                name, pwd = name_lst.strip().split(',')
                yield name, pwd

    @classmethod
    def login(cls,opt_dic):
        pwd = cls.get_md5(opt_dic)
        log.logging.info("login功能函数在进行登录验证时，调用了get_md5函数，生成密码的MD5值")
        with open(USER_INFO,encoding='utf-8') as f:
            for line in f:
                user,passwd = line.strip().split(',')
                if opt_dic['username'] == user and pwd == passwd:
                    # 保存当前登录用户,后续调用
                    cls.User = user
                    # 获取所有用户的目录
                    cls.Home_path = os.path.join(DB,'Home')
                    # 获取登录用户的家目录
                    cls.User_path = os.path.join(cls.Home_path,opt_dic['username'])
                    dic = {'username':opt_dic['username'],'operate': 'login', 'flag': True}
                    log.logging.info("用户：{}.登录验证成功,返回True".format(user))
                    break
            else:
                dic = {'username':opt_dic['username'],'operate': 'login', 'flag': False}
                log.logging.info("用户：{}.登录验证失败,返回False".format(user))
        return dic

    @classmethod
    def register(cls,opt_dic):
        pwd = cls.get_md5(opt_dic)
        log.logging.info("register功能函数在进行注册时，调用了get_md5函数，生成密码的MD5值")
        for name,pwds in cls.read_user(USER_INFO):
            # 判断用户是否存在
            if name == opt_dic['username']:
                # 返回False的字典
                dic = {'username':opt_dic['username'],'operate': 'register','flag':False}
                # 打印log
                log.logging.error("用户：{}.已存在,注册失败".format(opt_dic['username']))
                return dic
        else:
            with open(USER_INFO,mode='a',encoding='utf-8') as f:
                f.write('{},{}\n'.format(opt_dic['username'],pwd))
            # 获取所有用户的目录
            cls.Home_path = os.path.join(DB, 'Home')
            # 获取注册用户的家目录
            cls.User_path = os.path.join(cls.Home_path,opt_dic['username'])
            # 判断Home目录不存在创建
            if not os.path.exists(cls.Home_path): os.mkdir(cls.Home_path)
            # 判断用户目录不存在创建
            if not os.path.exists(cls.User_path): os.mkdir(cls.User_path)
            # 返回Trut的字典
            dic = {'username':opt_dic['username'],'operate': 'register','flag':True}
            # 打印log
            log.logging.info("用户：{}.注册成功,密码为：{}".format(opt_dic['username'],opt_dic['password']))
            return dic
    # 结束client的连接
    @classmethod
    def quit(cls,opt_dic):
        # 判断client发送过来的是否是Q
        if opt_dic['tag'] == 'Q':
            dic = {'operate':'quit','flag':True}
            return dic
        # 打印log
        log.logging.info("用户: {}.退出FTP程序".format(cls.User))
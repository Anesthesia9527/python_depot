#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/27 0029 10:35
# @Author : Zhaozhen
# @File : login.py
# @Software: PyCharm

from conf.settings import *
from core.base import File_oper


# 登录功能函数
def Login():
    print("\033[1;31;46m欢迎来到登录界面\033[0m".center(34, "#"))
    username,password = input("请输入  用户名：").strip(),input("请输入用户密码： ").strip()
    for name,pwd,ident in File_oper.read_user(user_info):
        if name == username and pwd == password:
            # 返回的是字典
            return {'state':True,'name':username,'ident':ident}
    else:
        # 返回的是字典
        return {'state':False,'name':username}
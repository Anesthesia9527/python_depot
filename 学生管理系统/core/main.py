#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/27 0025 21:22
# @Author : Zhaozhen
# @File : main.py
# @Software: PyCharm

import sys
from core.login import Login
from core.manager import Manager
from core.base import File_oper
from core.student import Student
from core import log

# 主函数
def Main():
    while True:
        print("\033[1;31;46m学生选课系统首页\033[0m".center(34, "#"))
        print('\t1、{}\n\t2、{}\n{}'.format('用户登录', '退出程序', ("#" * 27)))
        M = input("请输入操作序号：").strip()
        # 用户登录
        if M == '1':
            # 接受返回值
            ret = Login()
            # if判断True和False
            if ret['state']:
                print("用户：{} \033[031m登录成功\033[0m".format(ret['name']))
                # 写日志
                log.logging.info('用户：{} 登录学生选课系统.'.format(ret['name']))
                # 判断当前py文件中是否有此属性
                if hasattr(sys.modules[__name__],ret['ident']):
                    # 将内存地址赋值给cls
                    cls = getattr(sys.modules[__name__],ret['ident'])
                    # 实例化
                    obj = cls(ret['name'])
                    while True:
                        print("\033[1;31;46m欢迎到{}页面\033[0m".center(32, "#").format(ret['ident']))
                        # 打印功能菜单
                        for index,menu_lst in enumerate(cls.menu_lst,1):
                            print('\t{}、{}'.format(index,menu_lst[0]))
                        num = int(input("请输入要操作的序号："))
                        # 登录的用户的身份是Manager,num等于6或登录用户身份是Student,num等于4退出相对应的界面
                        if ret['ident'] == 'Manager' and num == 6 or ret['ident'] == 'Student' and num == 4:
                            log.logging.info('用户：{},退出{}页面.'.format(ret['name'],ret['ident']))
                            break
                        else:
                            # 否则就利用反射调用相应的方法
                            getattr(obj,cls.menu_lst[num-1][1])()
                else:
                    print("\033[031m无法识别此用户的身份\033[0m")
            else:
                # 写日志
                log.logging.error('用户：{},登录失败,用户名或密码错误.'.format(ret['name']))
                print("\033[031m登录失败,请重新尝试\033[0m")
        # 退出学生选课系统
        else:
            print("\033[031m已退出学生选课系统,欢迎您下次登录\033[0m")
            break





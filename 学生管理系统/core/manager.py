#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/27 0025 21:22
# @Author : Zhaozhen
# @File : manager.py
# @Software: PyCharm

from conf.settings import *
from core.course import Course
from core.base import File_oper
from core import log

# 管理员类
class Manager(File_oper):
    # 初始化
    def __init__(self, name):
        self.name = name

    # 管理员功能菜单
    menu_lst = [('创建课程','create_course'),('创建学生','create_student'),
                ('查看全部课程','show_course'),('查看全部学生','show_student'),
                ('查看全部学生选课情况','show_student_course'),('退出','exit')]

    # 创建课程
    def create_course(self):
        print("\033[1;031m创建课程输入格式\033[0m：课程名,课程周期,课程价格,授课老师")
        try:
            cou_name, cou_price, cou_period, cou_teacher = input("请输入要创建的课程：").strip().split(',')
            cou_obj = Course(cou_name,cou_price,cou_period,cou_teacher)
            with open(course_info,mode='a',encoding='utf-8') as f:
                f.write('{},{},{},{}\n'.format(cou_obj.name, cou_obj.price, cou_obj.period, cou_obj.teacher))
            print("[\033[032m{}\033[0m]课程,\033[031m创建完成\033[0m".format(cou_obj.name))
            # 写日志
            log.logging.info('用户：{},创建新的{}课程.'.format(self.name,cou_obj.name))
        except ValueError:
            log.logging.error('用户：{},创建新课程的时候,创建失败,应按格式输入：课程名,课程周期,课程价格,授课老师.'.format(self.name))
            print("课程创建失败")

    # 创建学生
    def create_student(self):
        stud_name,stud_pwd = input("请输入账号：").strip(),input("请输入账号密码：").strip()
        for name,pwd,ident in self.read_user(user_info):
            if name == stud_name:
                print('用户：{} 已存在'.format(stud_name))
                # 写日志
                log.logging.debug('用户：{},创建学生：{}时,提示用户已存在.'.format(self.name,stud_name))
                break
        else:
            self.write_user(user_info,stud_name,stud_pwd)
            # 创建学生账号的同时将此用户添加至student_info
            with open(student_info, mode='a', encoding='utf-8') as f:
                f.write('{}\n'.format(str({stud_name:[]})))
            print("学生账号：{} \033[031m创建成功\033[0m".format(stud_name))
            # 写日志
            log.logging.info('用户：{},创建新的学生账号：{} 密码：{}.'.format(self.name,stud_name,stud_pwd))

    # 全部课程显示
    def show_course(self):
        self.read_all_course(course_info)
        # 写日志
        log.logging.info('用户：{},查询系统全部的课程信息'.format(self.name))

    # 全部学生显示
    def show_student(self):
        print('\033[1;036m{}\033[0m:\n{:<11}{:<11}{:<11}'.format('全部学生显示', '学生账号', '学生密码', '学生身份'))
        for name,pwd,ident in self.read_user(user_info):
            # 判断身份是Student
            if ident == 'Student':
                print('{:<14}{:<14}{:<14}'.format(name, pwd, ident))
        # 写日志
        log.logging.info('用户：{},查询系统全部学生的信息.'.format(self.name))

    # 学生选课情况显示
    def show_student_course(self):
        print("\033[1;036m学生选课情况显示\033[0m：")
        for count,dic in enumerate(self.read_stud_cour(student_info),1):
            for name in dic:
                print('[学生{}] \033[031m{}\033[0m 选的课有：{}'.format(count,name,dic[name]))
        # 写日志
        log.logging.info('用户：{},查询系统学生选课的信息.'.format(self.name))



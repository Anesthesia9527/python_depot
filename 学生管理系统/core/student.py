#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/27 0025 21:22
# @Author : Zhaozhen
# @File : student.py
# @Software: PyCharm
from conf.settings import *
from core.base import File_oper
from core import log

class Student(File_oper):
    def __init__(self,name):
        self.name = name

    menu_lst = [('选择课程','choose_course'),('已选课程显示','has_choose_course'),
                ('全部课程显示','all_course_according'),('退出','exit')]
    # 选择课程
    def choose_course(self):
        # 显示全部课程
        self.read_all_course(course_info)
        new_core_str = []
        old_core_str = ""
        i_cou = input("请输入你选择的课程名称： ").strip()
        for dic in self.read_stud_cour(student_info):
            # for得到学生name
            for name in dic:
                # if学生name == 当前登录的学生name
                if self.name == name:
                    # 将name对应的课程列表添加到old_core_str
                    old_core_str += str(dic[name])
                    # 在将old_core_str转成列表并添加到new_core_str
                    new_core_str.append(eval(old_core_str))
                    # 将选择的新课程添加到new_core_str
                    new_core_str[0].append(i_cou)
                    break
        # 将旧的列表和新的列表传值给write_stud_cour
        self.write_stud_cour(student_info,self.name, old_core_str, str(new_core_str[0]))
        print("\033[031m恭喜你\033[0m,选择了[\033[031m{}\033[0m]这门课程.".format(i_cou))
        log.logging.info('用户:{},选择新的课程{}.'.format(self.name,i_cou))

    # 已选课程显示
    def has_choose_course(self):
        for dic in self.read_stud_cour(student_info):
            # for得到name
            for name in dic:
                # if-name是否等于当前登录的name,如果是显示所选择的课程
                if name == self.name:
                    print('\033[1;036m你选择的课程有\033[0m：{}'.format(dic[name]))
        log.logging.info('用户：{},查询自己选择的课程.'.format(self.name))
    # 全部课程显示、
    def all_course_according(self):
        # 调用read_all_course显示全部课程
        self.read_all_course(course_info)
        log.logging.info('用户：{},查询系统全部的课程.'.format(self.name))
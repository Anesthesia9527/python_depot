#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/27 0025 21:22
# @Author : Zhaozhen
# @File : base.py
# @Software: PyCharm

# 定义文件操作类
class File_oper:
    # 读取用户信息
    @staticmethod
    def read_user(path):
        with open(path,mode='r',encoding='utf-8') as f:
            for name_lst in f:
                name, pwd, iden = name_lst.strip().split('-')
                yield name, pwd, iden

    # 添加学生
    @staticmethod
    def write_user(path,name,pwd):
        with open(path,mode='a',encoding='utf-8') as f:
            f.write('{}-{}-Student\n'.format(name, pwd))

    # 读取学生已选课程信息
    @staticmethod
    def read_stud_cour(path):
        with open(path, mode='r', encoding='utf-8') as f:
            for stud_cour_lst in f:
                stud_cour_lst = eval(stud_cour_lst)
                yield stud_cour_lst

    # 添加学生选择的课程
    @staticmethod
    def write_stud_cour(path,name,old_str, new_str):
        file_data = ""
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                ret = eval(line.strip())
                for i in ret:
                    if i == name and old_str in line:
                        line = line.replace(old_str, new_str)
                    file_data += line
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_data)

    # 显示全部课程
    @staticmethod
    def read_all_course(path):
        print('\033[1;036m全部课程显示\033[0m：\n{:<12}{:<12}{:<12}{:<12}'.
              format('课程名字', '课程周期', '课程价格', '授课教师'))
        with open(path,mode='r',encoding='utf-8') as f:
            for cou_lst in f:
                name,price,period,teacher = cou_lst.strip().split(',')
                print('{:<15}{:<15}{:<15}{:<15}'.format(name, price, period, teacher))

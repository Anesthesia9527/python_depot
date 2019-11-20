#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time : 2019/7/30 0030 15:53
@Author : 赵臻
@File : 博客园登录.py
@Software: PyCharm
'''
# 导入time模块
import time
# 创建空列表,判断是否已登录
login_status = []
# 定义年月份
t = time.strftime("%Y-%m-%d %H:%M:%S")

# 读取用户信息功能
def login_info():
    with open('login.txt',mode='r',encoding='utf-8') as f:
        for name_list in f:
            names,pwds = name_list.strip().split(',')
            yield names,pwds

# 定义登录功能
def login():
        print("账号登录".center(20,"#"))
        row = 0
        # 循环3次,退出登录功能
        while row < 3:
            name,pwd = input("请输入登录用户名: ").strip(),input("请输入登录用户密码: ").strip()
            # 将获取的
            for names,pwds in login_info():
                if name == names and pwd == pwds:
                    print("恭喜你,使用用户：\033[031m%s\033[0m,登录成功"%name)
                    # 登录之后将用户名添加至login_stat列表,
                    login_status.append(name)
                    return True
            else:
                # 判断用户输入错误还剩几次机会
                if int(2 - row) != 0:
                    print("用户名或密码错误,还有\033[031m%s\033[0m次输入机会" % int(2 - row))
                    row += 1
                # 超过3次并自动退出程序
                else:
                    print("\033[031m>>>\033[0m输入错误3次,退出程序")
                    break
# 定义注册功能
def registered():
    print("账号注册".center(20, "#"))
    row = 0
    #循环3次,退出注册功能
    while row < 3:
        name,pwd = input("请输入注册用户名：").strip(),input("请输入注册用户密码： ").strip()
        # for循环如果判断用户是否存在于用户文件
        for names,_ in login_info():
            if name == names:
                row += 1
                if row < 3:
                    print("用户\033[031m%s\033[0m存在,还有\033[031m%s\033[0m次输入机会"%(name,int(3 - row)))
                    break
                else:
                    print("\033[031m>>>\033[0m输入错误3次,退出程序")
                    break
        # 如果不在并添加至用户文件
        else:
            # 将用户名及密码追加至用户信息文件
            with open('login.txt',mode='a',encoding='utf-8')as f1:
                f1.write('\n{},{}'.format(name, pwd))
                print("[用户:\033[031m%s\033[0m,密码:\033[031m%s\033[0m].注册成功,已自动登录"%(name,pwd))
            # 将注册信息追加至operate.log
            with open('operate.log', mode='a', encoding='utf-8') as f2:
                f2.write("User.registration.log {}的时候有新用户注册,用户名为：{} 密码为: {}\n".format(t, name, pwd))
                # 注册完用户之后实现自动登录,将用户添加至login_status列表
                login_status.append(name)
                return True
# 定义登录装饰器
def login_wrapper(func):
    def inner(*args,**kwargs):
        if login_status:
            ret = func()
            return ret
        else:
            print("你未登录,请先登录...")
            if login():
                ret = func()
                return ret
    return inner

# 定义日志装饰器
def log_wrapper(func):
    def inner(*args,**kwargs):
        # 将用户查询的记录追加至operate.log
        with open("operate.log",mode='a',encoding='utf-8') as f:
            f.write("User.login.log 用户：{} 在{}的时候 执行了{}函数\n".format(login_status[0],t,func.__name__))
        ret = func(*args,**kwargs)
        return ret
    return inner

@login_wrapper
@log_wrapper
# 文章页面功能
def article_page():
    print("欢迎\033[031m%s\033[0m访问文章页面"% login_status[0])

@login_wrapper
@log_wrapper
# 日志页面功能
def diary_page():
    print("欢迎\033[031m%s\033[0m访问日记页面"% login_status[0])

@login_wrapper
@log_wrapper
# 评论页面功能
def comment_page():
    print("欢迎\033[031m%s\033[0m访问评论页面"% login_status[0])

@login_wrapper
@log_wrapper
# 收藏页面功能
def collect_page():
    print("欢迎\033[031m%s\033[0m访问收藏页面"% login_status[0])

# 用户注销功能
def login_out():
    print("\033[031m%s\033[0m用户已注销"% login_status[0])
    # 清空login_status列表
    login_status.clear()

# 退出程序功能
def login_exit():
    print("退出程序..等着你回来哦")
    exit()

# 根据函数名可被赋值后调用,创建序列号对应的功能函数名字典
main_menu_dic = {1:login,2:registered,3:article_page,4:diary_page,5:comment_page,6:collect_page,7:login_out,8:login_exit}

def Boke_login():
    # while循环来调用所有功能,实现博客园登录
    while True:
        # 定义博客园登录功能菜单
        menu_bar = "#######\033[031m欢迎来到博客园首页\033[0m#######\n\t1. {}\n\t2. {}\n\t3. {}\n\t" \
                   "4. {}\n\t5. {}\n\t6. {}\n\t7. {}\n\t8. {}\n##############################".format\
            ('请登录', '请注册','文章页面', '日记页面', '评论页面', '收藏页面', '注销','退出程序')
        print(menu_bar)
        serial_number = int(input("请输入功能编号： "))
        # 判断用户输入的值是否>0,<=7
        if serial_number > 0 and serial_number <= 8:
            # 根据所定义的main_menu_dic字典调用各功能
            main_menu_dic[serial_number]()
            time.sleep(1)
        else:
            print("sorry,输入编号不在可选范围")
Boke_login()
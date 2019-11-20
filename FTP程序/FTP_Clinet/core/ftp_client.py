#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/9 0009 15:10
# @Author : Zhaozhen
# @File : ftp_client.py
# @Software: PyCharm

import os
import json
import sys
import time
from core.user_auth import UserOperation
from core.send_recv import SendAndRecv
from core.progress_bar import progres

class FilePutGet:

    @staticmethod
    def put(sk):
        print("\033[1;31;46m文件上传页面\033[0m".center(34, "#"))
        file_path = input("请输入上传的文件名路径：").strip()
        # 获取文件的MD5,文件名,文件大小
        filemd5,filename,filesize = SendAndRecv.get_md5(file_path),os.path.basename(file_path),os.path.getsize(file_path)
        dic = {'filename': filename, 'filesize': filesize, 'filemd5': filemd5, 'operate': 'put'}
        SendAndRecv.send_dic(sk, dic)
        # 接受server端发送的状态码
        status = SendAndRecv.recv_dic(sk)
        # 判断状态是否是可上传
        if status['status_code'] == 200:
            # 设置new_size初始值,用于结束while
            new_size = 0
            with open(file_path,'rb') as f:
                # 判断filesize是大于0,while不结束
                while filesize > 0:
                    # 每次读取4096字节
                    content = f.read(4096)
                    sk.send(content)
                    new_size += len(content)
                    # 调用进度条模块
                    progres(new_size,filesize,'文件上传中')
                    # 判断new_size大于等于本地文件的filesize就结束while循环
                    if new_size >= filesize:
                        break
            print('\t{}.已上传完成!'.format(filename))
        # 判断状态是否是断点续传
        elif status['status_code'] == 201:
            with open(file_path,'rb') as f:
                # 定义已传字节数
                f.seek(status['filesize'])
                # 判断server发送过来的文件字节数小于本地文件字节大小,while不结束
                while status['filesize'] < filesize:
                    # 每次读取4096字节
                    content = f.read(4096)
                    sk.send(content)
                    status['filesize'] += len(content)
                    # 将内容刷出内存
                    sys.stdout.write('\r')
                    # 调用进度条模块
                    progres(status['filesize'],filesize,'文件断点续传中')
                    # 如果最后已传的字节数大于等于本地文件的字节大小就结束循环
                    if status['filesize'] >= filesize:
                        break
            print('\t{}.已断点续传完成!'.format(filename))

    @staticmethod
    def s_file(sk):
        dic = {'operate':'get'}
        SendAndRecv.send_dic(sk,dic)
        # 接受server发送过来可下载的文件列表
        ret = SendAndRecv.recv_dic(sk)
        # 循环打印
        for index,file in enumerate(ret,1):
            print("{}、{}".format(index, file[0]))
        file_name = input("请输入下载的文件名：").strip()
        return file_name,ret

    @classmethod
    def get(cls,sk):
        print("\033[1;31;46m文件下载页面\033[0m".center(34, "#"))
        # 接受s_file的返回值,拿到文件名和文件列表
        file_name,ret = cls.s_file(sk)
        # 使用列表推导式拿到下载文件的元组
        file_size_lst = [i for i in ret if file_name in i]
        # 获取下载文件的大小
        file_size = file_size_lst[0][1]
        # 文件路径拼接
        file_path = os.path.join(UserOperation.User_path,file_name)
        # 定义字典文件名
        dic = {'filename':file_name}
        # 发送给server,告诉server要下载的是哪个文件
        SendAndRecv.send_dic(sk,dic)
        # 接受从server端发送过来的文件的MD5值
        ser_md5 = SendAndRecv.recv_dic(sk)
        # 判断本不存在此文件就下载
        if not os.path.exists(file_path):
            # 定义可下载的状态码
            dic = {'status_code':200}
            SendAndRecv.send_dic(sk,dic)
            with open(file_path,'wb') as f:
                size = 0
                # 如果所发送的文件字节数大于0,while不结束
                while file_size > 0:
                    # 每次接受4096个字节
                    content = sk.recv(4096)
                    f.write(content)
                    size += len(content)
                    # 调用进度条模块
                    progres(size,file_size, '文件下载中')
                    if size >= file_size:
                        break
            print("\t{}.已下载完成".format(file_name))
        # 获取已下载文件的MD5值
        cli_md5 = SendAndRecv.get_md5(file_path)
        # 判断如果本地文件的MD5值不等于server文件的MD5值就调用断点下载
        if ser_md5 != cli_md5:
            mp = input("{}.文件md5值存不一致,请输入y.n进行重新下载：".format(file_name))
            if mp.upper() == 'Y':
                # 获取本地文件的大小
                file_lenby = os.stat(file_path).st_size
                # 定义字典包含：文件名,状态码,未下载文成的文件大小
                dic = {'filename': file_name,'status_code':201,'filesize':file_lenby}
                SendAndRecv.send_dic(sk,dic)
                with open(file_path,'ab') as f:
                    size = file_lenby
                    # 如果本地文件字节数小于所下载文件的字节大小就不结束循环
                    while file_lenby < file_size:
                        # 每次接受4096字节数
                        content = sk.recv(4096)
                        f.write(content)
                        # 每次size加接受到的字节数
                        size += len(content)
                        # 调用进度条模块
                        progres(size,file_size,'文件断点下载中')
                        if size >= file_size:
                            break
                print('\t{}.已断点下载完成!'.format(file_name))
            # 判断为N就不继续断点下载
            elif mp.upper() == 'N':
                return
    @staticmethod
    def show_file(sk):
        # 获取登录用户的属主目录
        file_path = UserOperation.User_path
        # 判断此目录有文件
        if os.listdir(file_path):
            print('\033[1;036m{}\033[0m:\n{:<8}{:<8}{:<8}   {:<8}'.format('目前存在的文件','序号','文件属主','文件大小(字节)','文件名'))
            for index,file in enumerate(os.listdir(file_path),1):
                # 获取每个文件的大小
                file_size = os.path.getsize(os.path.join(file_path,file))
                print(' {:<10} {:<10}  {:<10} {:<10}'.format(index,UserOperation.User,file_size,file))
        # 如果属主目录为空提示下载
        else:
            print("\033[031m你的属主文件目录没有存在文件,请前往FTP操作页下载即可!\033[0m")



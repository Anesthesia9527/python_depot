#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/9 0009 21:16
# @Author : Zhaozhen
# @File : ftp_server.py
# @Software: PyCharm

import os
import sys
import hashlib
import json
from core.user_auth import Auth
from core.send_recv import SendAndRecv
from core import log

class FilePutGet:

    # 获取未上传完成文件的MD5
    @staticmethod
    def get_md5(file):
        if (os.path.exists(file)):
            md5 = hashlib.md5()
            with open(file, 'rb') as f:
                str = f.read()
                md5.update(str)
            file_md5 = md5.hexdigest()
            return file_md5

    # 文件上传
    @classmethod
    def put(cls,request,opt_dic):
        # 获取从client发送过来要上传文件的文件名，大小，MD5值
        filename,filesize,filemd5 = opt_dic['filename'],opt_dic['filesize'],opt_dic['filemd5']
        # 获取上传文件在server要保存的位置
        file_path = os.path.join(Auth.User_path,filename)
        # 判断是否存在此文件
        if not os.path.exists(file_path):
            dic = {'filename':filename,'status_code':200}
            # 向client发送状态码
            request.send(json.dumps(dic).encode('utf-8'))
            with open(file_path, 'wb') as f:
                # 判断要上传的文件字节数大于0 while循环不结束
                while opt_dic['filesize'] > 0:
                    # 每次接受4096字节数
                    content = request.recv(4096)
                    f.write(content)
                    opt_dic['filesize'] -= len(content)
                    # 跳出while循环
                    if opt_dic['filesize'] <= 0:
                        break
            # 打印log
            log.logging.info("用户：{}.上传了文件{}".format(Auth.User,filename))
        # 获取已上传的文件的MD5值
        file_md5 = cls.get_md5(file_path)
        # 判断client和server文件的MD5值是否一致
        if filemd5 != file_md5:
            # 获取未下载完成的文件的字节大小
            file_lenby = os.stat(file_path).st_size
            dic = {'filename': filename,'status_code':201,'filesize':file_lenby}
            # 发送dic到client
            request.send(json.dumps(dic).encode('utf-8'))
            with open(file_path,'ab') as f:
                # 定义size初始值
                size = file_lenby
                # 如果server端文件字节数小于要下载文件的字节数大小
                while file_lenby < filesize:
                    # 每次接受4096
                    content = request.recv(4096)
                    f.write(content)
                    size += len(content)
                    # 结束循环
                    if size >= filesize:
                        break
            # 打印log
            log.logging.info("用户：{}.调用了断点续传,上传了文件：{}".format(Auth.User,filename))

    # 向客户端发送可下载的文件列表
    @staticmethod
    def show_file(request):
        file_ = []
        file_path = 'E:\PyCharm代码目录\Python_oldbay\day10\day10_FTP作业\FTP_Server\db\Home\data_file'
        # 获取可下载文件的列表
        file_lst = os.listdir(file_path)
        for i in file_lst:
            # 获取每个文件的大小
            file_size = os.path.getsize(os.path.join(file_path,i))
            # 添加至file_
            file_.append((i,file_size))
        # 发送至client
        request.send(json.dumps(file_).encode('utf-8'))
        # 打印log
        log.logging.info("用户：{}.调用了show_file函数,向客户端发送了可下载的文件".format(Auth.User))
        return file_path

    # 定义上传文件的功能函数
    @classmethod
    def get(cls,request,_):
        # 接受可下载文件的目录
        file_ = cls.show_file(request)
        file_dic = SendAndRecv.myrecv(request)
        # 拼接文件的全路径
        file_path= os.path.join(file_,file_dic['filename'])
        # 获取文件的大小
        file_size = os.path.getsize(file_path)
        # 获取文件的MD5值
        ser_md5 = cls.get_md5(file_path)
        SendAndRecv.mysend(request,ser_md5)
        # 接受状态码
        status = SendAndRecv.myrecv(request)
        if status['status_code'] == 200:
            # 定义初始值
            new_size = 0
            with open(file_path, 'rb') as f:
                # 文件的file_size大于0，while不结束
                while file_size > 0:
                    # 每次发送4096字节数
                    content = f.read(4096)
                    request.send(content)
                    new_size += len(content)
                    # 结束while循环,文件发送完成
                    if new_size >= file_size:
                        break
            # 打印log
            log.logging.info("用户：{}.下载了文件：{}".format(Auth.User,file_dic['filename']))
        # 状态码为201,执行断点续传
        elif status['status_code'] == 201:
            with open(file_path,'rb') as f:
                # 使用seek定义值已传字节数位置
                f.seek(status['filesize'])
                # client未下载完成文件的字节数小于本地文件的字节数,while不结束
                while status['filesize'] < file_size:
                    # 每次发送4096字节数
                    content = f.read(4096)
                    request.send(content)
                    status['filesize'] += len(content)
                    # 将内容刷出内存
                    sys.stdout.write('\r')
                    # 结束while循环
                    if status['filesize'] >= file_size:
                        break
            # 打印log
            log.logging.info("用户：{}.下载文件：{}.失败并调用了文件断点下载功能".format(Auth.User,file_dic['filename']))









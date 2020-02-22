#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
from urllib.parse import quote
import ssl
import Env

ssl._create_default_https_context = ssl._create_unverified_context
JChost = Env.env()[1]

# 查询系统时间
def JCgetCurrentDate():
    url = JChost + '/getCurrentDate'
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    print(response)


# 修改系统时间
def JCsetCurrentDate(date):
    url = JChost + '/setCurrentDate/' + date
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    print(response)


# 根据姓名删除锦程额度
def JCmoveLimitByName(name):
    name2 = quote(name.encode('utf-8'))
    print(name)
    url = JChost + '/moveLimitByName/' + name2
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    if response == '无此额度信息或已删除':
        print('无此额度信息或已删除')
    elif response == '更新成功':
        print('成功删除该客户锦程额度')
    else:
        print('调用锦程葵花宝典-根据姓名删除额度，执行异常！')


# 根据申请号修改放款中状态为失败：F表示放款失败
def JCsetLoanStatusF(applyno):
    url = JChost + '/setLoanStatus/' + applyno + '/F'
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    print(response)


# 根据申请号修改放款中状态为成功：S是放款成功
def JCsetLoanStatusS(applyno):
    url = JChost + '/setLoanStatus/' + applyno + '/S'
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    print(response)


# 还款状态修改为成功等待回调
def JCrepaysetSuccess(applyno, amount):
    url = JChost + '/setSuccess/' + applyno + '/' + amount
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    print(response)


# 还款状态修改为失败的状态等待回调
def JCrepaysetFail(applyno, amount):
    url = JChost + '/setFail/' + applyno + '/' + amount
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    print(response)


# 跑批
def JCrunAll():
    url = JChost + '/runAll'
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    print(response)

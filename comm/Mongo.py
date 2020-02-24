#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import Env
from comm import Mysql
import configparser, os

# config.ini文件路径
configpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
# 读取数据库信息
business = Env.env()[2]
# 定义mysql数据库封装类对象
Mysql = Mysql.MysqlDB()

class MongoDB():

    def conn(self, table):
        # 读取config.ini配置文件
        config = configparser.ConfigParser()
        config.read(configpath, encoding='UTF-8')
        host = config.get("mongodb", "host")
        user = config.get("mongodb", "user")
        password = config.get("mongodb", "password")
        # 连接mongo
        client = MongoClient(host, 8717)
        # 连接mydb数据库,账号密码认证
        db = client.fintell_credit
        db.authenticate(user, password)
        collection = db[table]
        return collection

    # 获取mongo库integrationMessage表存储的三方数据，获取按照时间倒叙排列第一个
    def get_thirdpartydata(self, apiName, phone):
        collection = MongoDB().conn('integrationMessage')
        # sort() 方法第一个参数为要排序的字段，第二个字段指定排序规则，1 为升序，-1 为降序，默认为升序
        try:
            result = collection.find({"apiName": apiName, "input.phone": phone}).sort("createDate", -1)[0]
            input = result.get('input')
            output = result.get('output')
            datasourceInput = result.get('datasourceInput')
            datasourceOutput = result.get('datasourceOutput')
            # print('三方数据存入mongo库数据:\n', result)
            # print('input内容为:\n', input)
            print('output内容为:\n', output)
            # print('datasourceInput内容为:\n', datasourceInput)
            print('datasourceOutput内容为:\n', datasourceOutput)
        except:
            print('mongo库无查询结果')

    # 将mongo库三方数据有效期改为0
    def update_thirdpartydata(self, apiName, phone):
        collection = MongoDB().conn('integrationMessage')
        #  修改集合中所有满足条件的文档：multi: true
        try:
            collection.find({"apiName": apiName, "input.phone": phone})
            collection.update({"apiName": apiName, "input.phone": phone}, {'$set': {'effectiveTime': 0}},multi=True)
            print('将Mongo库中三方数据有效期改为0')
        except:
            print('mongo库无查询结果')

    # 获取业务系统加工入引擎的业务字段
    def get_GRXX(self, phone, engine, GRXXlist):
        sql = 'select apply_no from mag_customer_apply where tel=%s'
        apply_no = Mysql.selectwithparams(business, sql, phone)[0]
        collection = MongoDB().conn('creditRequest')
        # sort() 方法第一个参数为要排序的字段，第二个字段指定排序规则，1 为升序，-1 为降序，默认为升序
        result = collection.find({"creditRequestParam.data.applyNo": apply_no, "engineId": engine}).sort("createDate", -1)[0]
        if result != None:
            creditRequestParam = result.get('creditRequestParam')
            data = creditRequestParam.get('data')
            # print(result)
            print('业务系统加工入引擎业务字段:'.center(30, '*'))
            print(creditRequestParam, '\n')
            for GRXX in GRXXlist:
                if GRXX not in data.keys():
                    print(GRXX + ' 字段没有进行加工')
                else:
                    GRXXvalue = data.get(GRXX)
                    print(GRXX + ' 字段值：', GRXXvalue)
        else:
            print('mongo库无查询结果')




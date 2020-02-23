#!/usr/bin/python
# -*- coding: utf-8 -*-
from alpbusiness import Credit, Loan
from comm import ChangeEngine, GetResult, Mongo, Mysql
import alpbusiness.RequestDataSql as RequestDataSql
from apibase import JCapi
import unittest, time, Env
# 读取数据库信息
business, platform, rule = Env.env()[2], Env.env()[3], Env.env()[4]
# 定义mysql数据库封装类对象
Mysql, Mongo = Mysql.MysqlDB(), Mongo.MongoDB()

tel, name, card = '13000000001', '用户1', '110101190202174170'
channel = 'Android'  # 申请渠道：Android, IOS
engine = '386'
periods, amount = '6', '100'
GRXXlist=['GRXX1007', 'GRXX1002', 'GRXX1111']
process = 'Loan'

class Test_GRXX(unittest.TestCase):
    '''授信申请，获取入引擎的业务字段'''
    def test_GRXX(self):
        if process=='Credit':
            # ChangeEngine.changeCreditEngine(channel=channel, engine1=engine, engine2='344', engine3='345')   # 修改授信引擎
            alreadyapply = Mysql.selectwithparams(business, 'select count(*) from mag_customer_apply where tel=%s', tel)[0]
            if alreadyapply == '0':
                Credit.credit(name=name, card=card, tel=tel, channel=channel)  # 额度申请
            else:
                Credit.credittimes(name=name, tel=tel, channel=channel)  # 二次额度申请
            Mongo.get_GRXX(phone=tel, engine=int(engine), GRXXlist=GRXXlist)
        elif process=='Loan':
            # ChangeEngine.changeLoanEngine(channel=channel, engine=engine)   # 修改提现引擎
            alreadybandbankcard = Mysql.selectwithparams(business,'select count(*) from mag_bank_info where customer_id=(select id from mag_customer where tel=%s)',tel)[0]
            if alreadybandbankcard == '0':
                Loan.bankcard(tel=tel, channel=channel)
            Loan.loan(tel=tel, periods=periods, amount=amount, channel=channel)  # 提现申请
            Mongo.get_GRXX(phone=tel, engine=int(engine), GRXXlist=GRXXlist)
            Loan.changeloaninfo(tel=tel, loanresult='F')


    '''清除用户数据'''
    def test_Cleardata(self):
        JCapi.JCmoveLimitByName(name)
        Mysql.deletecustomer(business, tel)

#!/usr/bin/python
# -*- coding: utf-8 -*-
from alpbusinessprocesse import Credit, Loan
from comm import ChangeEngine, GetResult, Mongo, Mysql, CheckMysqlData
import alpbusinessprocesse.RequestDataSql as RequestDataSql
from apibase import JCapi
import unittest, time, Env
# 读取数据库信息
business, platform, rule = Env.env()[2], Env.env()[3], Env.env()[4]
# 定义mysql数据库封装类对象
Mysql, Mongo = Mysql.MysqlDB(), Mongo.MongoDB()

tel = '13000000001'
name = '用户'
card = '110101190202174170'
channel = 'Android'  # 申请渠道：Android, IOS
engine = '386'
periods, amount = '6', '100'

class Test_Business(unittest.TestCase):
    '''清除用户信息'''
    def test_001(self):
        JCapi.JCmoveLimitByName(name=name)
        Mysql.deletecustomer(business, tel=tel)

    '''录入用户信息'''
    def test_002(self):
        Credit.saveuserinfo(name=name, card=card, tel=tel, channel=channel)

    '''首次额度申请'''
    def test_003(self):
        Credit.credit(name=name, card=card, tel=tel, channel=channel)

    '''二次额度申请'''
    def test_004(self):
        Credit.credittimes(name=name, tel=tel, channel=channel)

    '''绑卡'''
    def test_005(self):
        Loan.bankcard(tel=tel, channel=channel)

    '''提现'''
    def test_006(self):
        Loan.loan(tel=tel, periods=periods, amount=amount, channel=channel)
        Loan.changeloaninfo(tel=tel, loanresult='S')  # S 放款成功变，更借据数据，能它能够还款； F 放款失败

    '''修改授信引擎'''
    def test_007(self):
        ChangeEngine.changeCreditEngine(channel=channel, engine1=engine, engine2='344', engine3='345')

    '''修改提现引擎'''
    def test_008(self):
        ChangeEngine.changeLoanEngine(channel=channel, engine=engine)

    '''校验数据落库'''
    def test_009(self):
        CheckMysqlData.MysqlData(tel)


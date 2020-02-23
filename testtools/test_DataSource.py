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

tel = '13000000001'
name = '用户1'
card = '110101190202174170'
channel = 'Android'  # 申请渠道：Android, IOS
engine = '386'
periods, amount = '6', '100'
apiName = 'LUCHENG_PHONESCORE'   # DUXIAOMAN_BLACKLEVEL   DUXIAOMAN_LOANSSCORE   LUCHENG_PHONESCORE

class Test_datasource(unittest.TestCase):

    '''授信申请，获取引擎报告，获取mongo库存储的三方数据'''
    def test_001(self):
        ChangeEngine.changeCreditEngine(channel=channel, engine1=engine, engine2='344', engine3='345')   # 修改授信引擎
        alreadyapply = Mysql.selectwithparams(business, 'select count(*) from mag_customer_apply where tel=%s', tel)[0]
        if alreadyapply == '0':
            Credit.credit(name=name, card=card, tel=tel, channel=channel)  # 额度申请
        else:
            Credit.credittimes(name=name, tel=tel, channel=channel)  # 二次额度申请
        time.sleep(10)
        print('引擎报告'.center(60,'*'))
        GetResult.getruleresult(process='Credit', tel=tel, engine=engine)   # 获取引擎报告
        print('mongo库integrationMessage表存储的三方数据'.center(50, '*'))
        Mongo.get_thirdpartydata(apiName=apiName, phone=tel)  # 获取mongo库integrationMessage表存储的三方数据
        Mongo.update_thirdpartydata(apiName=apiName, phone=tel)  # 将mongo库三方数据有效期改为0

    '''提现申请，获取引擎报告，获取mongo库存储的三方数据'''
    def test_002(self):
        ChangeEngine.changeLoanEngine(channel=channel, engine=engine)   # 修改提现引擎
        alreadybandbankcard = Mysql.selectwithparams(business,
                                                 'select count(*) from mag_bank_info where customer_id=(select id from mag_customer where tel=%s)', tel)[0]
        if alreadybandbankcard == '0':
            Loan.bankcard(tel=tel, channel=channel)
        Loan.loan(tel=tel, periods=periods, amount=amount, channel=channel)  # 提现申请
        time.sleep(5)
        print('引擎报告'.center(30, '*'))
        GetResult.getruleresult(process='Loan', tel=tel, engine=engine)   # 获取引擎报告
        print('mongo库integrationMessage表存储的三方数据'.center(50, '*'))
        Mongo.get_thirdpartydata(apiName=apiName, phone=tel)  # 获取mongo库integrationMessage表存储的三方数据
        Mongo.update_thirdpartydata(apiName=apiName, phone=tel)  # 将mongo库三方数据有效期改为0
        Loan.changeloaninfo(tel=tel, loanresult='S')  # 若产生借据则修改借据状态为放款失败

    '''清除用户数据'''
    def test_003(self):
        JCapi.JCmoveLimitByName(name)
        Mysql.deletecustomer(business, tel)

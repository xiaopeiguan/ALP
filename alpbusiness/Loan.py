#!/usr/bin/python
# -*- coding: utf-8 -*-
import apibase.Appapi as Appapi
import apibase.JCapi as JCapi
from comm import Mysql, ChangeEngine, GetResult, Mongo
import alpbusiness.RequestDataSql as RequestDataSql
import json, time, datetime, random, string
import Env

# 读取数据库信息
business, platform, rule = Env.env()[2], Env.env()[3], Env.env()[4]
# 定义mysql数据库封装类对象
Mysql, Mongo = Mysql.MysqlDB(), Mongo.MongoDB()


def login(tel, channel):
    if channel == 'Android':
        r = Appapi.login(RequestDataSql.androidlogindata(tel))
        Appapi.apiprint('登录', RequestDataSql.androidlogindata(tel), r)
    elif channel == 'IOS':
        r = Appapi.login(RequestDataSql.ioslogindata(tel))
        Appapi.apiprint('登录', RequestDataSql.ioslogindata(tel), r)
    elif channel == 'H5':
        r = Appapi.login(RequestDataSql.H5logindata(tel))
        Appapi.apiprint('登录', RequestDataSql.H5logindata(tel), r)
    else:
        print('暂不支持' + channel + '渠道')

# 绑卡设置交易密码
def bankcard(tel, channel):
    # 获取用户编号、客户编号
    id = Mysql.selectwithparams(business, RequestDataSql.getid, tel)[0]
    customer_id = Mysql.selectwithparams(business, RequestDataSql.getcustomerid, tel)[0]
    # 登陆
    login(tel, channel)
    # 银行卡OCR识别接口
    r = Appapi.bankCard(RequestDataSql.bankCarddata())
    Appapi.apiprint('银行卡OCR识别接口', RequestDataSql.bankCarddata(), r)
    bank_card_number = r.json().get('retData').get('bank_card_number')
    # 保存OCR次数
    r = Appapi.sendOCRTime(RequestDataSql.sendOCRTimedata(id, '4'))
    Appapi.apiprint('保存OCR次数', RequestDataSql.sendOCRTimedata(id, '4'), r)
    # 绑卡发送验证码接口
    r = Appapi.bindCardSendSmsCode(RequestDataSql.bindCardSendSmsCodedata(tel, customer_id, bank_card_number))
    Appapi.apiprint('绑卡发送验证码接口', RequestDataSql.bindCardSendSmsCodedata(tel, customer_id, bank_card_number), r)
    request_no = r.json().get('retData')
    # 绑卡校验验证码接口
    r = Appapi.bindCardCheckSmsCode(RequestDataSql.bindCardCheckSmsCodedata(tel, customer_id, request_no, bank_card_number))
    Appapi.apiprint('绑卡校验验证码接口', RequestDataSql.bindCardCheckSmsCodedata(tel, customer_id, request_no, bank_card_number), r)
    # 修改银行卡自动还款接口
    bankcard_id = Mysql.selectwithparams(business, RequestDataSql.getbankid, tel)[0]
    r = Appapi.updateBank(RequestDataSql.updateBankdata(bankcard_id))
    Appapi.apiprint('修改银行卡自动还款接口', RequestDataSql.updateBankdata(bankcard_id), r)
    # 设置支付密码接口 交易密码=111111
    r = Appapi.updatePassWord(RequestDataSql.updatePassWorddata(customer_id))
    Appapi.apiprint('设置支付密码接口', RequestDataSql.updatePassWorddata(customer_id), r)

# 提现申请
def loan(tel, periods, amount, channel):
    # 获取用户编号、客户编号
    id = Mysql.selectwithparams(business, RequestDataSql.getid, tel)[0]
    customer_id = Mysql.selectwithparams(business, RequestDataSql.getcustomerid, tel)[0]
    # 登陆
    login(tel, channel)
    # 交易密码校验接口
    r = Appapi.checkPayPassword(RequestDataSql.checkPayPassworddata(customer_id))
    Appapi.apiprint('交易密码校验接口', RequestDataSql.checkPayPassworddata(customer_id), r)
    # 申请进件接口
    r = Appapi.createOrder(RequestDataSql.createOrderdata(customer_id, periods, amount))
    Appapi.apiprint('申请进件接口', RequestDataSql.createOrderdata(customer_id, periods, amount), r)
    # 查询放款审批结果
    time.sleep(5)
    GetResult.getloanresult(tel)


# 变更借据数据
# 调锦程葵花宝典为放款成功 -> 等待借据状态变成‘还款中’ -> 修改mysql库借据申请时间 -> 调锦程葵花宝典修改系统时间为明天 -> 跑批
def changeloaninfo(tel, loanresult):
    applyno = Mysql.selectwithparams(business, RequestDataSql.selectapplno, tel)[0]
    state1 = Mysql.selectwithparams(business, RequestDataSql.getloanstate, tel)[0]
    if applyno != None and state1 == '1':
        print('订单审核中')
    elif applyno != None and state1 == '2':
        print('订单失效')
    elif applyno != None and state1 == '3':
        print('申请提现成功，借据状态为‘放款中’。开始进行放款结果回调...')
        if loanresult =='S':
            # 调锦程葵花宝典为放款成功
            JCapi.JCsetLoanStatusS(applyno)
            # 查看借据状态变成‘还款中’
            time.sleep(60)
            state2 = Mysql.selectwithparams(business, RequestDataSql.getloanstate, tel)[0]
            if state2 !='6':
                time.sleep(70)
                state3 = Mysql.selectwithparams(business, RequestDataSql.getloanstate, tel)[0]
                if state3 !='6':
                    print('放款成功可能没有回调，看下日志吧')
                else:
                    print('放款成功已回调，借据状态为‘还款中’')
                    # 修改mysql库借据申请时间
                    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
                    newcreatetime = datetime.datetime.strftime(yesterday, '%Y%m%d%H%M%S')
                    params = (newcreatetime, tel)
                    Mysql.updatewithparams(business, RequestDataSql.updateloancreatetime, params)
                    # 调锦程葵花宝典修改系统时间为明天
                    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
                    date = datetime.datetime.strftime(tomorrow, '%Y%m%d')
                    JCapi.JCsetCurrentDate(date)
                    # 跑批
                    JCapi.JCrunAll()
                    print('借据可以进行还款操作了')
            else:
                print('放款成功已回调，借据状态为‘还款中’')
                # 修改mysql库借据申请时间
                yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
                newcreatetime = datetime.datetime.strftime(yesterday, '%Y%m%d%H%M%S')
                params = (newcreatetime, tel)
                Mysql.updatewithparams(business, RequestDataSql.updateloancreatetime, params)
                # 调锦程葵花宝典修改系统时间为明天
                tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
                date = datetime.datetime.strftime(tomorrow, '%Y%m%d')
                JCapi.JCsetCurrentDate(date)
                # 跑批
                JCapi.JCrunAll()
                print('借据可以进行还款操作了')
        elif loanresult == 'F':
            # 调锦程葵花宝典为放款失败
            JCapi.JCsetLoanStatusF(applyno)
            time.sleep(60)
            state4 = Mysql.selectwithparams(business, RequestDataSql.getloanstate, tel)[0]
            if state4 == '5':
                print('放款失败回调成功')
            else:
                time.sleep(65)
                state5 = Mysql.selectwithparams(business, RequestDataSql.getloanstate, tel)[0]
                if state5 == '5':
                    print('放款失败回调成功')
                else:
                    print('放款失败可能没有回调，看下日志吧')
        else:
            print('放款回调结果输入错误')
    elif applyno != None and state1 == '4':
        print('审批拒绝')
    elif applyno != None and state1 == '5':
        print('放款失败')
    elif applyno != None and state1 == '6':
        print('申请提现成功，借据状态为‘还款中’')
    elif applyno != None and state1 == '7':
        print('借据已结清')
    else:
        print('提现异常了')


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

# 提前还款
def advancerepay(tel, applyno, prepayAmt, repayresult):
    # 获取用户编号、客户编号
    id = Mysql.selectwithparams(business, RequestDataSql.getid, tel)[0]
    customer_id = Mysql.selectwithparams(business, RequestDataSql.getcustomerid, tel)[0]
    jcLtNo = Mysql.selectwithparams(business, RequestDataSql.getjcLtNo, tel)[0]
    state= Mysql.selectwithparams(business, 'select state from mag_order where applNo=%s', applyno)[0]
    if state == '6':
        # 登录
        r = Appapi.login(RequestDataSql.androidlogindata(tel))
        Appapi.apiprint('登录', RequestDataSql.androidlogindata(tel), r)
        # # 借据还款接口
        # r = Appapi.repayreceipt(RequestDataSql.repayreceiptdata(jcLtNo))
        # Appapi.apiprint('借据还款接口', RequestDataSql.repayreceiptdata(jcLtNo), r)
        # 判断借据日期是否是当天
        r = Appapi.isCanRepay(RequestDataSql.isCanRepaydata(applyno))
        Appapi.apiprint('判断借据日期是否是当天', RequestDataSql.isCanRepaydata(applyno), r)
        # 还款计划查询接口
        r = Appapi.repaymentPlanList(RequestDataSql.repaymentPlanListdata(applyno))
        Appapi.apiprint('还款计划查询接口', RequestDataSql.repaymentPlanListdata(applyno), r)
        # 显示银行卡信息接口
        r = Appapi.getBank(RequestDataSql.getBankdata(customer_id))
        Appapi.apiprint('显示银行卡信息接口', RequestDataSql.getBankdata(customer_id), r)
        # 提前还款金额计算接口
        r = Appapi.partRepayTry(RequestDataSql.partRepayTrydata(applyno, prepayAmt))
        Appapi.apiprint('提前还款金额计算接口', RequestDataSql.partRepayTrydata(applyno, prepayAmt), r)
        repaymentAmount = r.json().get('retData').get('repaymentAmount')
        # 线上还款接口
        r = Appapi.directRepay(RequestDataSql.directRepaydata(applyno, repaymentAmount))
        Appapi.apiprint('线上还款接口', RequestDataSql.directRepaydata(applyno, repaymentAmount), r)
        code = r.jaon.get('retData').get('code')
        if code == 'E0001':
            if repayresult == 'S':
                JCapi.JCrepaysetSuccess(applyno, repaymentAmount)  # 还款状态修改为成功等待回调
                time.sleep(60)
                state1 = Mysql.selectwithparams(business,
                                                'select state from mag_repayment_record where appl_no=%s order by create_time desc limit 1',
                                                applyno)[0]
                if state1 == '1':
                    print('还款状态修改为成功已回调')
                else:
                    print('请查看还款状态修改为成功回调状态')
            elif repayresult == 'F':
                JCapi.JCrepaysetFail(applyno, repaymentAmount)  # 还款状态修改为成功等待回调
                time.sleep(60)
                state1 = Mysql.selectwithparams(business,
                                                'select state from mag_repayment_record where appl_no=%s order by create_time desc limit 1',
                                                applyno)[0]
                if state1 == '2':
                    print('还款状态修改为失败已回调')
                else:
                    print('请查看还款状态修改为失败回调状态')
        else:
            print('线上还款异常了，看下日志吧')
    else:
        print('借据状态不是还款中，请查看')


if __name__ == '__main__':
    tel ='13000000001'
    prepayAmt ='100'
    applyno = '20200530041240'
    repayresult = 'S'   # S: 还款状态修改为成功等待回调； F: 还款状态修改为失败等待回调
    advancerepay(tel, applyno, prepayAmt, repayresult)
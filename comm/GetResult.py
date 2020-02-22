#!/usr/bin/python
# -*- coding: utf-8 -*-
from comm import Mysql
import Env
import alpbusinessprocesse.RequestDataSql as RequestDataSql
import json

# 读取数据库信息
business = Env.env()[2]
platform = Env.env()[3]
rule = Env.env()[4]
# 定义mysql数据库封装类对象
Mysql = Mysql.MysqlDB()

# 获取额度申请结果
def getcreditresult(tel):
    print('获取额度申请结果'.center(30, '*'))
    refuse_code = Mysql.selectwithparams(business, RequestDataSql.getapplystate, tel)[0]
    print('apply_state: ' + refuse_code + ' (1:通过，0:拒绝，2:人工审核，3:系统审核中)')
    if refuse_code == '1':
        credit_amount = Mysql.selectwithparams(business, RequestDataSql.getamount, tel)[0]
        print('额度申请结果： 通过' + '  获得额度： ' + credit_amount)
    elif refuse_code == '0':
        rule_refuse_node = Mysql.selectwithparams(business, RequestDataSql.getrefusecode, tel)[0]
        print('额度申请结果： 拒绝' + '  拒绝原因： ' + rule_refuse_node)
    elif refuse_code == '2':
        print('额度申请结果： 进入人工审核')
    elif refuse_code == '3':
        print('额度申请结果： 系统审核中')
    else:
        print('请手动查看额度申请结果！')

# 获取提现申请结果
def getloanresult(tel):
    print('获取提现审批结果'.center(30, '*'))
    state = Mysql.selectwithparams(business, RequestDataSql.selectorderstate, tel)[0]
    print('提现审批状态： ' + state + ' (1订单审核中，2失效订单，3放款中(审批通过)，4审批拒绝，5放款失败，6还款中(放款成功)，7已结清订单)')
    if state == '1':
        print('提现审批结果： 订单审核中')
    elif state == '3':
        applNo = Mysql.selectwithparams(business, RequestDataSql.selectapplno, tel)[0]
        print('提现审批结果： 放款中(审批通过)' + '  applNo： ' + applNo)
    elif state == '4':
        decision_reject_reason = Mysql.selectwithparams(business, RequestDataSql.selectloanrefusecode, tel)[0]
        print('提现审批结果： 审批拒绝' + '  拒绝原因： ', decision_reject_reason)
    elif state == '5':
        print('提现审批结果： 放款失败')
    else:
        print('可能提现申请异常了，手动查看吧！')

# 获取规则引擎报告结果，获取规则列表。若拒绝，则进一步获取拒绝规则名称
def getruleresult(process, tel,engine):
    params = (tel, engine)
    if process == 'Credit':
        rulehaserror = 1
        sql = 'select risk_state from mag_risk_info where customer_id=(select id from mag_customer where tel=%s) and risk_num=%s order by create_time desc limit 1'
        risk_state = Mysql.selectwithparams(business, sql, params)[0]
        if risk_state == '0' or risk_state == '4':
            print('风控异常了，看下日志吧')
            return rulehaserror
        else:
            sql1 = 'select pid from mag_risk_info where customer_id=(select id from mag_customer where tel=%s) and risk_num=%s order by create_time desc limit 1'
            pid = Mysql.selectwithparams(business, sql1, params)[0]
            sql2 = 'select result, id, input from zw_resultset where batch_no=%s'
            result, id, input = Mysql.selectwithparams(rule, sql2, pid)[0], Mysql.selectwithparams(rule, sql2, pid)[1], Mysql.selectwithparams(rule, sql2, pid)[2]
            if result == '通过':
                print(engine + '引擎结果为： ' + result)
                print(engine + '引擎规则列表为： ' + input)
            elif result == '拒绝':
                print(engine + '引擎结果为： ' + result)
                print(engine + '规则列表为： ' + input)
                sql3 = 'select name, remark from zw_resultset_list where resultset_id=%s'
                name, remark = Mysql.selectwithparams(rule, sql3, id)[0], Mysql.selectwithparams(rule, sql3, id)[1]
                print('用户申请被 (' + name + ' ' + remark + ') 拒绝')
            rulehaserror = 0
            return rulehaserror
    elif process == 'Loan':
        sql4 = 'select pid from mag_risk_info where customer_id=(select id from mag_customer where tel=%s) and risk_num=%s order by create_time desc limit 1'
        pid = Mysql.selectwithparams(business, sql4, params)[0]
        sql5 = 'select result, id, input from zw_resultset where batch_no=%s'
        result, id, input = Mysql.selectwithparams(rule, sql5, pid)[0], Mysql.selectwithparams(rule, sql5, pid)[1], Mysql.selectwithparams(rule, sql5, pid)[2]
        if result == '通过':
            print(engine + '引擎结果为： ' + result)
            print(engine + '引擎规则列表为： ' + input)
        elif result == '拒绝':
            print(engine + '引擎结果为： ' + result)
            print(engine + '规则列表为： ' + input)
            sql6 = 'select name, remark from zw_resultset_list where resultset_id=%s'
            name, remark = Mysql.selectwithparams(rule, sql6, id)[0], Mysql.selectwithparams(rule, sql6, id)[1]
            print('用户申请被 (' + name + ' ' + remark + ') 拒绝')
    else:
        print('请输入 process = Credit 或 Loan')






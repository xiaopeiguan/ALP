#!/usr/bin/python
# -*- coding: utf-8 -*-
from comm import Mysql
import Env

# 读取数据库信息
business = Env.env()[2]
platform = Env.env()[3]
# 定义mysql数据库封装类对象
Mysql = Mysql.MysqlDB()

# 变更授信引擎编号
def changeCreditEngine(channel, engine1, engine2, engine3):
    if channel == 'Android':
        sql1 ='update zw_sys_dict set name = %s where parent_id = "420" and code = "engine1"'
        sql2 = 'update zw_sys_dict set name = %s where parent_id = "420" and code = "engine2"'
        sql3 = 'update zw_sys_dict set name = %s where parent_id = "420" and code = "engine3"'
    elif channel == 'IOS':
        sql1 ='update zw_sys_dict set name = %s where parent_id = "766" and code = "engine1"'
        sql2 = 'update zw_sys_dict set name = %s where parent_id = "766" and code = "engine2"'
        sql3 = 'update zw_sys_dict set name = %s where parent_id = "766" and code = "engine3"'
    elif channel == 'H5':
        sql1 ='update zw_sys_dict set name = %s where parent_id = "899" and code = "engine1"'
        sql2 = 'update zw_sys_dict set name = %s where parent_id = "899" and code = "engine2"'
        sql3 = 'update zw_sys_dict set name = %s where parent_id = "899" and code = "engine3"'
    elif channel == 'fp_rz':
        sql1 ='update zw_sys_dict set name = %s where parent_id = "882" and code = "engine1"'
        sql2 = 'update zw_sys_dict set name = %s where parent_id = "882" and code = "engine2"'
        sql3 = 'update zw_sys_dict set name = %s where parent_id = "882" and code = "engine3"'
    elif channel == 'fp_jd':
        sql1 ='update zw_sys_dict set name = %s where parent_id = "905" and code = "engine1"'
        sql2 = 'update zw_sys_dict set name = %s where parent_id = "905" and code = "engine2"'
        sql3 = 'update zw_sys_dict set name = %s where parent_id = "905" and code = "engine3"'
    elif channel == 'fp_jdjt':
        sql1 ='update zw_sys_dict set name = %s where parent_id = "909" and code = "engine1"'
        sql2 = 'update zw_sys_dict set name = %s where parent_id = "909" and code = "engine2"'
        sql3 = 'update zw_sys_dict set name = %s where parent_id = "909" and code = "engine3"'
    elif channel == 'qts':
        sql1 ='update zw_sys_dict set name = %s where parent_id = "924" and code = "engine1"'
        sql2 = 'update zw_sys_dict set name = %s where parent_id = "924" and code = "engine2"'
        sql3 = 'update zw_sys_dict set name = %s where parent_id = "924" and code = "engine3"'
    else:
        print('暂不支持' + channel + '渠道')
    Mysql.updatewithparams(business, sql1, engine1)
    # Mysql.updatewithparams(business, sql2, engine2)
    # Mysql.updatewithparams(business, sql3, engine3)

# 变更提现引擎编号
def changeLoanEngine(channel, engine):
    if channel == 'Android':
        sql = 'update zw_sys_dict set name = %s where parent_id = "794" and code = "alp_android"'
    elif channel == 'IOS':
        sql = 'update zw_sys_dict set name = %s where parent_id = "794" and code = "alp_ios"'
    elif channel == 'H5':
        sql = 'update zw_sys_dict set name = %s where parent_id = "794" and code = "alp_h5"'
    elif channel == 'fp_rz':
        sql = 'update zw_sys_dict set name = %s where parent_id = "794" and code = "fp_rz"'
    elif channel == 'fp_jd':
        sql = 'update zw_sys_dict set name = %s where parent_id = "794" and code = "fp_jd"'
    else:
        print('暂不支持' + channel + '渠道')
    Mysql.updatewithparams(business, sql, engine)
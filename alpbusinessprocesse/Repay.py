#!/usr/bin/python
# -*- coding: utf-8 -*-
import apibase.Appapi as Appapi
import apibase.JCapi as JCapi
from comm import Mysql, ChangeEngine, GetResult
import alpbusinessprocesse.RequestDataSql as RequestDataSql
import json, time, datetime, random, string
import Env

# 读取数据库信息
business = Env.env()[2]
platform = Env.env()[3]
rule = Env.env()[4]
# 定义mysql数据库封装类对象
Mysql = Mysql.MysqlDB()


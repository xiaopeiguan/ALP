#!/usr/bin/python
# -*- coding: utf-8 -*-
from comm import Mysql
import webbrowser
import os
import Env

selectsqlpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfile', 'selectsql.txt')
htmlpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfile', 'html.html')

# 读取数据库信息
business = Env.env()[2]
# 定义mysql数据库封装类对象
Mysql = Mysql.MysqlDB()

def titlelist():
    # 用户信息
    titlelist1 = ['用户手机号', '用户编号', '客户编号', '渠道号', '平台号', '姓名', '性别', '年龄', '身份证号', '户籍地址', '身份证有效期', '活体得分(0-1)',
                  '活体识别照片比对分数(0-1)', '人脸公安验证结果(1通过，0未通过)', '人脸识别状态(1通过，0未通过)', '人脸图片锦程方路径', '身份证正面锦程方路径', '身份证反面锦程方路径']
    # 个人信息
    titlelist2 = ['月收入', '学历', '居住地址', '详细居住地址', '公司名称', '公司地址', '详细公司地址']
    # 联系人信息
    titlelist3 = ['联系人1姓名', '联系人1电话', '联系人1关系', '联系人2姓名', '联系人2电话', '联系人2关系']
    # 设备信息
    titlelist4 = ['设备类型', '设备品牌', '设备型号', '操作系统', 'imei', 'oaid', '网络类型', 'wifiname', 'IP地址', 'wifiMac', '申请省份', '申请市',
                  '申请区', '申请地理位置', '纬度', '经度']
    # 额度信息
    titlelist5 = ['产品名称', '年利率', '锦程额度申请流水号jcLtNo', '预授信额度', '总额度', '剩余额度', '是否过期', '是否销户', '是否冻结']
    titlelist = titlelist1 + titlelist2 + titlelist3 + titlelist4 + titlelist5
    return titlelist


def getvaluelist(tel):
    with open(selectsqlpath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        file.close()
        valuelist = []
        for line in lines:
            sql = str(line).replace('19900000000', tel)
            value = Mysql.selectwithoutparams(business, sql)[0]
            # 生成结果列表
            valuelist.append(value)
    return valuelist


def getlist(titlelist, valuelist):
    list = []
    for i in range(0, len(titlelist)):
        a = []
        a.append(titlelist[i])
        a.append(valuelist[i])
        tup = tuple(a)
        list.append(tup)
    print(list)
    return list


def tohtml(list):
    head1 = '<html><head><meta charset="utf-8"></head><body>'
    head2 = '</body></html>'
    with open(htmlpath, "w", encoding='utf-8') as htmlfile:
        htmlfile.write(head1)
        htmlfile.write('\n')
    for a in list:
        body = '<p>%s的值是 : %s</p>' % (a[0], a[1])
        with open(htmlpath, "a", encoding='utf-8') as htmlfile:
            htmlfile.write(body)
            htmlfile.write('\n')
    with open(htmlpath, "a", encoding='utf-8') as htmlfile:
        htmlfile.write(head2)
        htmlfile.close()

def MysqlData(tel):
    list = getlist(titlelist(), getvaluelist(tel))
    tohtml(list)
    # 运行完自动在网页中显示
    webbrowser.open(htmlpath, new=1, autoraise=True)



#!/usr/bin/python
# -*- coding: utf-8 -*-
import Env
import apibase.RequestMethodJC as RequestMethodJC
import json

host = Env.env()[0]  # 获取主机
s = RequestMethodJC.headers()
method = 'POST'
requestType = 'data'


# 打印接口调用结果
def apiprint(name, data, r):
    print(name)
    print(data)
    print(r.text)
    # retCode = json.loads(r.text)['retCode']
    # if retCode == 'SUCCESS':
    #     print('接口调用SUCCESS')
    # elif retCode == 'JC_SUCCESS':
    #     print('调用锦程接口SUCCESS')
    # else:
    #     print('接口调用FAIL')
    # print('\n')


# 登录
def login(data):
    url = host + '/login/login'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 注册
def register(data):
    url = host + '/reg/register'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 新注册接口
def doRegister(data):
    url = host + '/reg/doRegister'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 发送验证码
def reggetSmsCode(data):
    url = host + '/reg/getSmsCode'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 请求产品选择页面
def getProductInfo(data):
    url = host + '/product/getProductInfo'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 申请产品
def applyProduct(data):
    url = host + '/product/applyProduct'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 身份信息回显
def getIdentityInfoByCustId(data):
    url = host + '/authorization/getIdentityInfoByCustId'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# OCR校验接口
def checkOCRTimes(data):
    url = host + '/authorization/checkOCRTimes'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 保存OCR次数
def sendOCRTime(data):
    url = host + '/authorization/sendOCRTime'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 身份证正面OCR识别
def idCardFront(data):
    url = host + '/discernApi/idCardFront'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 身份证反面OCR识别
def idCardBack(data):
    url = host + '/discernApi/idCardBack'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 保存身份信息
def saveIndentityInfo(data):
    url = host + '/authorization/saveIndentityInfo'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 个人信息回显接口
def getBasicInfo(data):
    url = host + '/basicinfo/getBasicInfo'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 个人信息保存接口
def addPersonInfo(data):
    url = host + '/basicinfo/addPersonInfo'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 联系人信息回显接口
def getLinkMan(data):
    url = host + '/authorization/getLinkMan'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 联系人信息保存接口
def upLinkMan(data):
    url = host + '/authorization/upLinkMan'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 保存设备信息及地理位置信息接口
def addDeviceInfo(data):
    url = host + '/basicinfo/addDeviceInfo'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 保存通话记录接口
def saveCallRecord(data):
    url = host + '/basicinfo/saveCallRecord'
    method = 'POST'
    requestType = 'data'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 安心签开户
def getAnXinQianAccount(data):
    url = host + '/order/getAnXinQianAccount'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 维护提示接口
def maintenanceinfo(data):
    url = host + '/maintenance/info'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 获取活体token接口
def getBizToken(data):
    url = host + '/discernApi/getBizToken'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 安卓额度审批接口
def CreditForRisk(data):
    url = host + '/order/CreditForRisk'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# ios额度审批接口
def CreditForIosRisk(data):
    url = host + '/order/CreditForIosRisk'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 首页展示接口
def producthomePage(data):
    url = host + '/product/homePage'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 获取完成度接口
def basicinfogetComplete(data):
    url = host + '/basicinfo/getComplete'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 获取支持银行列表信息接口
def getSupportBankList(data):
    url = host + '/msg/getSupportBankList'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 显示银行卡信息接口
def getBank(data):
    url = host + '/basicinfo/getBank'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 银行卡OCR识别接口
def bankCard(data):
    url = host + '/discernApi/bankCard'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 绑卡发送验证码接口
def bindCardSendSmsCode(data):
    url = host + '/basicinfo/bindCardSendSmsCode'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 绑卡校验验证码接口
def bindCardCheckSmsCode(data):
    url = host + '/basicinfo/bindCardCheckSmsCode'
    method = 'POST'
    requestType = 'data'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 修改银行卡自动还款接口
def updateBank(data):
    url = host + '/basicinfo/updateBank'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 设置支付密码接口
def updatePassWord(data):
    url = host + '/basicinfo/updatePassWord'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 借款页面接口
def getOrderPageInfo(data):
    url = host + '/order/getOrderPageInfo'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 交易密码校验接口
def checkPayPassword(data):
    url = host + '/basicinfo/checkPayPassword'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 申请进件接口
def createOrder(data):
    url = host + '/order/createOrder'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 检查系统时间是否在锦程禁止还款时间段内
def checkTimePeriod(data):
    url = host + '/product/checkTimePeriod'
    method = 'POST'
    requestType = 'data'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 判断借据还款是否可以展示数据
def isShowRepay(data):
    url = host + '/order/isShowRepay'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 借据还款接口
def repayreceipt(data):
    url = host + '/repay/receipty'
    method = 'POST'
    requestType = 'data'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 判断借据日期是否是当天
def isCanRepay(data):
    url = host + '/order/isCanRepay'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 还款计划查询接口
def repaymentPlanList(data):
    url = host + '/repay/repaymentPlanList'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 部分提前还款金额计算接口
def partRepayTry(data):
    url = host + '/repay/partRepayTry'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# 线上还款接口
def directRepay(data):
    url = host + '/repay/directRepay'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# H5额度申请
def creditForH5Risk(data):
    url = host + '/order/creditForH5Risk'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r


# H5额度申请
def saveH5gid(data):
    url = host + '/authorization/saveH5gid'
    r = RequestMethodJC.sendrequest(s, url, method, requestType, data)
    return r

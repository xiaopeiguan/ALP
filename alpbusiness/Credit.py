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

# 注册
def register(tel, channel):
    # 清用户信息
    Mysql.deletecustomer(business, tel)
    # 注册获取验证码
    r1 = Appapi.reggetSmsCode(RequestDataSql.reggetSmsCodedata(tel))
    Appapi.apiprint('注册获取验证码', RequestDataSql.reggetSmsCodedata(tel), r1)
    time.sleep(2)
    smsCode = Mysql.selectwithparams(business, RequestDataSql.getsmscode, tel)[0]
    print('注册')
    if channel == 'Android':
        r2 = Appapi.doRegister(RequestDataSql.androiddoregisterdata(tel, smsCode))
    elif channel == 'IOS':
        r2 = Appapi.doRegister(RequestDataSql.iosdoregisterdata(tel, smsCode))
    elif channel == 'H5':
        r2 = Appapi.doRegister(RequestDataSql.H5doregisterdata(tel, smsCode))
    else:
        print('暂不支持' + channel + '渠道')
    print(r2.text)
    retCode = json.loads(r2.text)['retCode']
    retMsg = json.loads(r2.text)['retMsg']
    if retCode == 'FAIL':
        print('注册失败，提示信息： ' + retMsg + '\n')
    elif retCode == 'SUCCESS':
        print('注册成功' + '\n')
    time.sleep(2)
    id = Mysql.selectwithparams(business, RequestDataSql.getid, tel)[0]
    return id

# 登陆
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


# 身份认证
def saveauthentication(tel, channel):
    # 修改锦程系统时间为当前时间
    date = datetime.datetime.now().strftime('%Y%m%d')
    JCapi.JCsetCurrentDate(date)
    time.sleep(1)
    # 获取用户编号
    id = Mysql.selectwithparams(business, RequestDataSql.getid, tel)[0]
    # 登陆
    login(tel, channel)
    # 身份证正面OCR识别 刘童的身份证
    r1 = Appapi.idCardFront(RequestDataSql.idCardFrontdata())
    Appapi.apiprint('身份证正面OCR识别', RequestDataSql.idCardFrontdata(), r1)
    # 获取身份证识别信息
    person_name = r1.json().get('retData').get('result').get('name')
    card = r1.json().get('retData').get('result').get('number')
    customer_id = r1.json().get('retData').get('customer_id')
    card_register_address = r1.json().get('retData').get('result').get('address')
    Zcard_src = r1.json().get('retData').get('Zcard_src')
    # 保存OCR次数
    r = Appapi.sendOCRTime(RequestDataSql.sendOCRTimedata(id, '1'))
    Appapi.apiprint('保存OCR次数', RequestDataSql.sendOCRTimedata(id, '1'), r)
    # 身份证反面OCR识别 刘童的身份证
    r2 = Appapi.idCardBack(RequestDataSql.idCardBackdata())
    Appapi.apiprint('身份证反面OCR识别', RequestDataSql.idCardBackdata(), r2)
    # 获取身份证识别信息
    sign_date = r2.json().get('retData').get('result').get('sign_date')
    expiry_date = r2.json().get('retData').get('result').get('expiry_date')
    card_effective_time = sign_date + '-' + expiry_date
    Fcard_src = r2.json().get('retData').get('Fcard_src')
    # 保存OCR次数
    r = Appapi.sendOCRTime(RequestDataSql.sendOCRTimedata(id, '2'))
    Appapi.apiprint('保存OCR次数', RequestDataSql.sendOCRTimedata(id, '2'), r)
    # 保存身份信息
    r = Appapi.saveIndentityInfo(
        RequestDataSql.saveIndentityInfodata(person_name, card, id, customer_id, card_effective_time, card_register_address, Zcard_src, Fcard_src))
    Appapi.apiprint('保存身份信息', RequestDataSql.saveIndentityInfodata(person_name, card, id, customer_id, card_effective_time, card_register_address, Zcard_src, Fcard_src), r)

# mock身份证信息
def saveauthenticationmock(name, card, tel):
    sql = 'update mag_customer set PERSON_NAME = "' + name + '", card = "' + card + '" where tel = "' + tel + '"'
    Mysql.selectwithoutparams(business, sql)

# 个人信息
def savePersonInfo(tel, channel):
    # 获取客户编号
    customer_id = Mysql.selectwithparams(business, RequestDataSql.getcustomerid, tel)[0]
    # 登陆
    login(tel, channel)
    r = Appapi.addPersonInfo(RequestDataSql.addPersonInfodata(customer_id))
    Appapi.apiprint('个人信息保存接口', RequestDataSql.addPersonInfodata(customer_id), r)

# 联系人信息
def saveLinkManInfo(tel, channel):
    # 获取客户编号
    customer_id = Mysql.selectwithparams(business, RequestDataSql.getcustomerid, tel)[0]
    # 登陆
    login(tel, channel)
    # 联系人信息保存接口
    r = Appapi.upLinkMan(RequestDataSql.upLinkMandata(customer_id))
    Appapi.apiprint('联系人信息保存接口', RequestDataSql.upLinkMandata(customer_id), r)

def saveuserinfo(name, card, tel, channel):
    # 清除锦程方该客户额度
    JCapi.JCmoveLimitByName(name)
    id = register(tel, channel)
    # 登陆
    login(tel, channel)
    # 申请产品
    r = Appapi.applyProduct(RequestDataSql.applyProductdata(id))
    Appapi.apiprint('申请产品', RequestDataSql.applyProductdata(id), r)
    # 保存身份证、个人信息、联系人信息
    saveauthentication(tel, channel)
    saveauthenticationmock(name, card, tel)
    savePersonInfo(tel, channel)
    saveLinkManInfo(tel, channel)


def credit(name, card, tel, channel):
    # 清除锦程方该客户额度
    JCapi.JCmoveLimitByName(name)
    id = register(tel, channel)
    # 登陆
    login(tel, channel)
    # 申请产品
    r = Appapi.applyProduct(RequestDataSql.applyProductdata(id))
    Appapi.apiprint('申请产品', RequestDataSql.applyProductdata(id), r)
    # 保存身份证、个人信息、联系人信息
    saveauthentication(tel, channel)
    saveauthenticationmock(name, card, tel)
    savePersonInfo(tel, channel)
    saveLinkManInfo(tel, channel)
    # 获取客户编号
    customer_id = Mysql.selectwithparams(business, RequestDataSql.getcustomerid, tel)[0]
    # 登陆
    login(tel, channel)
    if channel == 'Android':
        # 保存设备信息及地理位置信息
        r = Appapi.addDeviceInfo(RequestDataSql.androidaddDeviceInfodata(customer_id))
        Appapi.apiprint('保存设备信息及地理位置信息接口', RequestDataSql.androidaddDeviceInfodata(customer_id), r)
        # 保存通话记录接口
        r = Appapi.saveCallRecord(RequestDataSql.androidsaveCallRecorddata(customer_id))
        Appapi.apiprint('保存通话记录接口', RequestDataSql.androidsaveCallRecorddata(customer_id), r)
    elif channel == 'IOS':
        r = Appapi.addDeviceInfo(RequestDataSql.iosaddDeviceInfodata(customer_id))
        Appapi.apiprint('保存设备信息及地理位置信息接口', RequestDataSql.iosaddDeviceInfodata(customer_id), r)
    else:
        print('暂不支持' + channel + '渠道')
    # 安心签开户
    r = Appapi.getAnXinQianAccount(RequestDataSql.getAnXinQianAccountdata(customer_id))
    Appapi.apiprint('安心签开户', RequestDataSql.getAnXinQianAccountdata(customer_id), r)
    # 人脸识别
    print('后台更新数据mock人脸识别' + '\n')
    mockfacesql = 'UPDATE mag_customer SET ALTER_TIME = "20190823172433", oss_face_key ="alp02/53b1754f1b928ecda45112401e2e3b91_20190925143347515.jpg", face_src ="https://ronghuialp.oss-cn-shenzhen.aliyuncs.com/alp02/7dbbbcdec97fa205bc1ded9a57fda42d_20190823172433200.jpg?Expires=1566552333&OSSAccessKeyId=LTAIvE2cfCGXURWc&Signature=ra4iAtrGeddIUF7Lu7pn05sdQd4%3D", person_face_state="1", person_face_complete="100", face_liveness_score = "1.0", face_verify_score= "1", face_verify_result ="1" WHERE ID = "' + customer_id + '"'
    Mysql.updatewithoutparams(business, mockfacesql)
    # # 修改channelcode已通过风控规则  APP -> 111
    # Mysql.updatewithparams(business, RequestDataSql.updatechannelcode, tel)
    if channel == 'Android':
        r = Appapi.CreditForRisk(RequestDataSql.CreditForRiskdata(customer_id))
        Appapi.apiprint('安卓额度审批接口', RequestDataSql.CreditForRiskdata(customer_id), r)
    elif channel == 'IOS':
        r = Appapi.CreditForIosRisk(RequestDataSql.CreditForIosRiskdata(customer_id))
        Appapi.apiprint('IOS额度审批接口', RequestDataSql.CreditForIosRiskdata(customer_id), r)
    else:
        print('暂不支持' + channel + '渠道')
    time.sleep(5)
    GetResult.getcreditresult(tel)

def credittimes(name, tel, channel):
    # 清除锦程方该客户额度
    JCapi.JCmoveLimitByName(name)
    # 获取客户编号
    customer_id = Mysql.selectwithparams(business, RequestDataSql.getcustomerid, tel)[0]
    # 清除拒绝原因
    Mysql.updatewithparams(business, RequestDataSql.deleterefusecode, tel)
    # 修改申请状态为拒绝
    Mysql.updatewithparams(business, RequestDataSql.updateapplystate, tel)
    # 修改额度为null
    Mysql.updatewithparams(business, RequestDataSql.updateamount, tel)
    # 修改channelcode已通过风控规则  APP -> 111
    Mysql.updatewithparams(business, RequestDataSql.updatechannelcode, tel)
    login(tel, channel)
    if channel == 'Android':
        r = Appapi.CreditForRisk(RequestDataSql.CreditForRiskdata(customer_id))
        Appapi.apiprint('安卓额度审批接口', RequestDataSql.CreditForRiskdata(customer_id), r)
    elif channel == 'IOS':
        r = Appapi.CreditForIosRisk(RequestDataSql.CreditForIosRiskdata(customer_id))
        Appapi.apiprint('IOS额度审批接口', RequestDataSql.CreditForIosRiskdata(customer_id), r)
    else:
        print('暂不支持' + channel + '渠道')
    time.sleep(5)
    GetResult.getcreditresult(tel)









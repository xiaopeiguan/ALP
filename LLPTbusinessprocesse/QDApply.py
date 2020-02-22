import base64
from Crypto.Cipher import AES
import hashlib
import time
import json
import requests

# 密钥（key）, 密斯偏移量（iv） CBC模式加密

def AES_Encrypt(key, data):
    # vi = '1234561234561234'
    vi = 'NesYXGBD2G3mHjKJ'
    pad = lambda s: s + (16 - len(s.encode('utf8')) % 16) * chr(16 - len(s.encode('utf8')) % 16)
    data = pad(data)
    # 字符串补位
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    # 加密后得到的是bytes类型的数据
    encodestrs = base64.b64encode(encryptedbytes)
    # 使用Base64进行编码,返回byte字符串
    enctext = encodestrs.decode('utf8')
    # 对byte字符串按utf-8进行解码
    return enctext

def AES_Decrypt(key, data):
    vi = '1234561234561234'
    data = data.encode('utf8')
    encodebytes = base64.decodebytes(data)
    # 将加密数据转换位bytes类型数据
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    text_decrypted = cipher.decrypt(encodebytes)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    # 去补位
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted


if __name__ == '__main__':
    AES_SECRETKEY_PASSWORD ='MfG2tqpMSQsIOmOx'
    AES_SECRETKEY_SIGN = 'MfG2tqpMSQsIOmOx'
    # data = '{"userId":"qd1579589247665"}'
    data = '{"bankMobileNo":"17112345682","bankName":"建设银行","bankNo":"6217003800012345678","belongsIndus":"200003","cardAddr":"北京市海淀区上园村3号院2014级经管学校","certExpiryDate":"20191227_20391226","companyAddress":"北京市海淀区安宁庄路小米科技园","companyName":"小米科技有限责任公司","createDate":"2020-01-21 14:47:27","deviceInfo":{"imei":"866347042130672","ipAddress":"119.57.163.66"},"education":"0","extInfo":{"modeScore":"99","qdCreditScore":"100","qdWealthScore":"10000"},"faceifCertSelfResults":1,"faceifCertSelfScore":100,"idCardNo":"11010119851007205X","maritalStatus":"S","mobileNo":"17112345682","name":"张五","notifyUrl":"http://localhost:8080/api/qd/vo/audit/apply","quotaNo":"E8517EC67666422F95F2BDD2EED9EAEA","residentialAddress":"北京市海淀区上园村3号院2014级经管学校","urgentContactMobile":"13112345678","urgentContactName":"张四","urgentContactRelationship":"4","userId":"qd1579589247665"}'
    data1 = AES_Encrypt(AES_SECRETKEY_PASSWORD, data)
    ts = str(int(round(time.time() * 1000)))
    data2 = data1+ts
    data3 = hashlib.md5(data2.encode(encoding='UTF-8')).hexdigest()
    data4 = AES_Encrypt(AES_SECRETKEY_SIGN, data3)
    # print(data1)
    print(data3)
    print(data4)
    applyBaseInfo_url = 'http://106.75.212.175:8886/api/qd/audit/apply'  # 额度授信接口#
    applyBaseInfo_body = {
        "reqId": "535EE5492EDB4162AA5412C2EA1F9924",
        "ts": ts,
        "sign": data4,
        "data": data1,
        "partnerId": "JCXJ001",
        "organizationId": "JC_QD_01"

    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=applyBaseInfo_url, json=applyBaseInfo_body)
    print(applyBaseInfo_body)
    print(response.text)
    print(response.status_code)

















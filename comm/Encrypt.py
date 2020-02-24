import base64
from Crypto.Cipher import AES
# Python的hashlib提供了常见的摘要算法，如MD5, SHA1、SHA224、SHA256、SHA384、SHA512和MD5算法等。
import hashlib
import json
import requests
import time


# MD5加密不可逆，生成32位的16进制字符串
# 加盐是在用户密码加密后，可以再加一个指定的字符串，再次加密
def md5data(data):
    md5data = hashlib.md5(data.encode(encoding='utf-8')).hexdigest()
    print(md5data)
    return md5data


def sha256data(data):
    sha256data = hashlib.sha256(data.encode(encoding='utf-8')).hexdigest()
    print(sha256data)
    return sha256data

'''
1.非对称加密解密会生成一对公钥和私钥,公钥公开,私钥自己持有.
2.加密是用来保证谁能获取消息明文
3.签名是用来保证消息是谁发送的
4.加密解密,签名验签都是用的非对称加解密实现的,名称和用法不一样,之所以不一样是因为非对称的机制决定的
总结：公钥和私钥是成对的，它们互相解密。公钥加密，私钥解密。私钥数字签名，公钥验证。
'''
def AES_Encrypt(key, data):
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

def decrypt():
    url = 'http://112.74.251.89:8081/cipher/decrypt'
    s = requests.Session()
    headers = {'content-type': 'application/json'}
    s.headers.update(headers)
    encryptKey = input('请输入encryptKey：\n')
    time.sleep(2)
    encryptData = input('请输入encryptData：\n')
    data = {
        "coopOrg": "alp_app_client",
        "orgIdPair": "alp_app_api|alp_app_client",
        "reqId": "d0ed137f-9c08-41f6-94e6-1441af1a54ca",
        "reqOrg": "alp_app_api",
        "reqParams": {
            "encryptData": encryptData,
            "encryptKey": encryptKey
        },
        "reqTime": "20190517155146",
        "sign": "5ba73fc11425126268bb6e2182b400eb"
    }
    r = requests.post(url=url, headers=headers, json=data)
    print('打印解密请求')
    decryptresult = r.json()
    result = json.dumps(decryptresult, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    print(result)


if __name__ == '__main__':
    md5data('用户5')

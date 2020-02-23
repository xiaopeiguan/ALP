import base64
from Crypto.Cipher import AES
import hashlib
import requests

def AES_Encrypt(key, data):
    vi = '1234561234561234'
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

def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


if __name__ == '__main__':
    key = '1234561234561234'
    tel = '13711111111'
    card = '110101199009077070'
    applyNo = '202002190011'
    # data = '{"userInfo":{"interestRate":"0.00050000","profession":"5","certType":"10100","idExpire":"20250108","cardAddr":"北京朝阳区蓝堡国际中心","address":"北京朝阳区蓝堡国际中心","activateTag":"UN_ACTIVATED","bkTel":"18724793302","contactName":"周小波","userTel":"'+ tel +'","cardNo":"'+ card +'","contactTel":"15011237677","applyAmount":"100000000","certNo":"11010119840922010X","contactRelation":"0301","pin":"狗狗和凤凤","bankNo":"6215982583010088792","username":"周小偲"},"identityInfo":{"facePhotoMatchLv":"1","reversePhoto":"/upload/cr/20181107/1060089611579035648/2013062320262198ReversePhoto.jpg","facePhoto":"/upload/cr/20181107/1060089611579035648/2013062320262198FacePhoto.jpg","personPDF":"/upload/cr/20181107/1060089611579035648/JK1048611968040329218.pdf","photoMatchLv":"1","creditReportPDF":"/upload/cr/20181107/1060089611579035648/JK1048611968040329218.pdf","creditQuotaPDF":"/upload/cr/20181107/1060089611579035648/JK1048611968040329218.pdf","frontPhoto":"/upload/cr/20181107/1060089611579035648/2013062320262198FrontPhoto.jpg"},"applyNo":"'+ applyNo +'","applyTime":"20190920112540","businessType":"JT"}'
    data = '{"userInfo":{"interestRate":"0.00050000","profession":"1","certType":"10100","idExpire":"20350830","address":"上海市上海市辖区张江高科ADDR","activateTag":"UN_ACTIVATED","bkTel":"'+ tel +'","contactName":"张三","userTel":"'+ tel +'","cardNo":"'+ card +'","contactTel":"13331180158","applyAmount":"100000000","certNo":"110101199009057141","contactRelation":"1","pin":"jd_5eae88eb7f43f","bankNo":"1111111","username":"杨一媛"},"identityInfo":{"facePhotoMatchLv":"1","reversePhoto":"/upload/cr/20181107/1060089611579035648/2013062320262198ReversePhoto.jpg","facePhoto":"/upload/cr/20181107/1060089611579035648/2013062320262198FacePhoto.jpg","personPDF":"/upload/cr/20181107/1060089611579035648/2013062320262198PersonPDF.jpg","photoMatchLv":"1","creditReportPDF":"/upload/cr/20181107/1060089611579035648/2013062320262198CreditReportPDF.jpg","creditQuotaPDF":"/upload/cr/20181107/1060089611579035648/2013062320262198CreditQuotaPDF.jpg","frontPhoto":"/upload/cr/20181107/1060089611579035648/2013062320262198FrontPhoto.jpg"},"applyNo":"'+ applyNo +'","applyTime":"20190920112540","businessType":"JT"}'
    # data = '{"userInfo":{"interestRate":"0.00050000","profession":"1","certType":"10100","idExpire":"20350830","address":"","activateTag":"UN_ACTIVATED","bkTel":"'+ tel +'","contactName":"张三","userTel":"'+ tel +'","cardNo":"'+ card +'","contactTel":"13331180158","applyAmount":"100000000","certNo":"110101199009057141","contactRelation":"1","pin":"jd_5eae88eb7f43f","bankNo":"1111111","username":"杨一媛"},"identityInfo":{"facePhotoMatchLv":"1","reversePhoto":"/upload/cr/20181107/1060089611579035648/2013062320262198ReversePhoto.jpg","facePhoto":"/upload/cr/20181107/1060089611579035648/2013062320262198FacePhoto.jpg","personPDF":"/upload/cr/20181107/1060089611579035648/2013062320262198PersonPDF.jpg","photoMatchLv":"1","creditReportPDF":"/upload/cr/20181107/1060089611579035648/2013062320262198CreditReportPDF.jpg","creditQuotaPDF":"/upload/cr/20181107/1060089611579035648/2013062320262198CreditQuotaPDF.jpg","frontPhoto":"/upload/cr/20181107/1060089611579035648/2013062320262198FrontPhoto.jpg"},"applyNo":"'+ applyNo +'","applyTime":"20190920112540","businessType":"JT"}'

    AES_Encrypt(key, data)
    enctext = AES_Encrypt(key, data)

 #生成签名#

salt = "789789"
datajd = enctext
stringSignTemp = datajd + "|" + salt
sign = md5(stringSignTemp)
print(enctext)
text_decrypted = AES_Decrypt(key, enctext)
print(text_decrypted)
print(len(text_decrypted))
print(sign)

#接口调用#

applyBaseInfo_url = 'http://106.75.212.187:8206/japi/v1/apply/audit'#额度授信接口#

# applyBaseInfo_url = 'http://106.75.211.232:9090/japi/v1/apply/audit/result'#授信结果查询接口#
#额度申请#
applyBaseInfo_body = {
  "requestNo":"157232212261714",
  "txCode":"CREDIT_APPLY",
  "version":"1.0",
  "channelCode":"JD_JT",
  "requestTime":"20190829113848",
  "requestData":enctext,
  "sysSign":sign
}
print(applyBaseInfo_body)
# print(type(applyBaseInfo_body))

headers = {'Content-Type':'application/json'}

response = requests.post(url=applyBaseInfo_url,json=applyBaseInfo_body)
print(response.text)
# print(response.url)
print(response.status_code)
print(response.content.decode("utf-8"))

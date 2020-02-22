# coding=gbk
import base64
from Crypto.Cipher import AES
import hashlib
# 密钥（key）, 密斯偏移量（iv） CBC模式加密

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
    # data = '被加密的字符串'
    data = "Vae27MezM6girNObcauHsGg2zty+LkLT3XFjYgfCmMEsH4BahIj4UM6kE+gtFshBkstWij6a3/2HD+btgA6AyjFhv87zLy1cfGfiObNL85Fhkog9zoR3OSRRPgxYyrC/9Woq6LU6pl80Bf4yCOSmR61PN/0kj0i4N+7zPlaq2RhPLQF0Q07VJcVq0Z46WeDYI+d3xw/p9LV0RtKqLFU6edg39Pv7w/ARDqDUpy93UMDIbC19ZyTRyCvNwCsyW1J7e+6mAx41BUX7wTZPTk0VhIO0CK7+gzAkVngxx7iWNTrSSmH0IcjcCEHuqllX5Y+FMU4VUdHU2V/oJ9rPKFegxUazKdRPtmeEa9QRipfStdWoT3mCy3R8RCaOMZfKk5dLC8J5+RTP5oVR/8nvRpF+FdL8DOW28MMAiYU4JXmfPZow5tVmk/q38VJizI43DOGw6SWAkZ2J5nJs1sUQiDfRARFMYwLiwr3TBTd4DjW74Fqjs7KoEnTjZCEeNIJ4k/XhSXNATLfhHN6e3d2qFuIEl1E1cPGFjVotmF4nfzK9WKZRCPhb5wYEPvamOwxGt1+D8w1PK6fgEVwKZ6RNVFzwAyDBRpIyCGM+aSzrMRGxrZtwTIh7s1+G7bP5D5wZ7XoWEJUp/XTW0WgUZ9DiUE07um38sXniQibWY0lM8a6WLitjWlTqgQJwOFDqaDDEzs6PeITL5Ge7B3Z+iIpPT5FkV2OvcvZheWzFLTLASZQDPbd2ZHqHCAIN9jSygEULsveHazCJWh4CbGu1qE9ugXcjAc5uDif0mMEiOqbSxEA7iAWaBGxh5st7DDCpLeGquW4MGewWrBakyAOltiI/du405tAg8ntTkkPawdKuDAtD8lzOAFi1Bsyo6ScUAIF+utyEq+MEUfPoB1mrTL3F0XWS71XmNMoC6Vb9KIsekS3SuLaY+MiPJId1aLVNoK9HOtWpHtNhNpIlbwgJ0xP5Bq1WBpLKCHNmgxkpNiO5Xxb1FaZLaZYzwIQKRh2aqNS82lkobzHYQoyRrRyWTE+/eVCfz6T09sWyWG0xIEf+CbpIbZbseZOOPt/ACxw7HVLrc8xHzbDRj9kZlc7rtf+58ZTQiPFdhJkZm+MyodrZICXZ62Oa/Wo6P8L1hDLIO1g0xcp5XDp27v9f4k7QfvZt+pOXwrl4NFF2BdnxIneRr/o0FU9aZFZ/R3W73aaNIR/6GBjtwerWKL7I8Lw93TNan3AgKiPUX9CfbBb+zsg4j0mXeQHvCs78YcNGCMF8Pbd/NmsVAH4Bug46B4vJXaQSlQcLD6bC/4/1EI5KlbVuUk4kDUTiqaEOK1oX8qZe/u5UeoVo3zA5+2Mj0DiMGvKuQHGSITKBrP/Ny102y1RHHb3nrJIztZpX/jefCLelSeMxK4V49nWeyCicDKXKW4NXTc/3t/7dCX4lhPp+pg56LpLaRmn9I+ZFOBB7/Knn+DtHkC5kdlNiiIUMA/IMpbpOnluppJ2eqG8xGxbaefUuc+SotiA="

    AES_Decrypt(key,data)
    dectext = AES_Decrypt(key,data)

 #生成签名#

salt = "789789"
# datajd = dectext
stringSignTemp = data + "|" + salt
sign = md5(stringSignTemp)
print("解密参数是:",dectext)


import requests


def headers():
    # session自动保存cookies，可以设置请求参数
    s = requests.Session()
    # session提供默认content-type数据
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    s.headers.update(headers)
    return s

# get 请求
def get(s, url, requestType, data):
    if requestType == 'param':
        r = s.get(url, params=data, verify=False)
        return r
    else:
        print('其他GET请求传参形式暂不支持')

# post 请求
def post(s, url, requestType, data):
    if requestType == 'data':
        r = s.post(url, data=data, verify=False)
        return r
    elif requestType == 'files':
        r = s.post(url, files=data, verify=False)
        return r
    elif requestType == 'json':
        r = s.post(url, json=data, verify=False)
        return r
    else:
        print('其他POST请求传参形式暂不支持')

# 发送接口请求重写request
def sendrequest(s, url, method, requestType, data):
    if method == 'GET':
        return get(s, url, requestType, data)
    elif method == 'POST':
        return post(s, url, requestType, data)
    else:
        print('输入的method暂不支持！')

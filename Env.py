import configparser
import os

# --------- 读取config.ini配置文件 ---------------
configpath = os.path.join(os.path.dirname(__file__), 'config.ini')  # config.ini文件路径
config = configparser.ConfigParser()
config.read(configpath, encoding='utf-8')

huanjing = 'uat1' # 选择测试环境

def env():
    if huanjing == 'sit1':
        host = config.get("host", "sit1host")
        JChost = 'https://117.174.24.234:4018/sit1'
        business = 'sit1mysqlbusiness'
        platform = 'sit1mysqlplatform'
    elif huanjing == 'uat1':
        host = config.get("host", "uat1host")
        JChost = 'https://117.174.24.234:4018/uat1'
        business = 'uat1mysqlbusiness'
        platform = 'uat1mysqlplatform'
    elif huanjing == 'uat2':
        host = config.get("host", "uat2host")
        JChost = 'https://117.174.24.234:4018/uat2'
        business = 'uat2mysqlbusiness'
        platform = 'uat2mysqlplatform'
    else:
        print('输入的环境暂不支持，请再config.ini文件中添加环境信息！')
    rule = 'mysqlrule'
    return host, JChost, business, platform, rule




if __name__ == '__main__':
    print(env())


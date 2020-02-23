import pymysql
import configparser, os, time, traceback

deletesqlpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testfile', 'deletesql.txt')  # deletesql.txt文件路径
configpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')  # config.ini文件路径

class MysqlDB():
    # 连接数据库
    def conn(self, mysqlname):
        # 读取config.ini配置文件
        config = configparser.ConfigParser()
        config.read(configpath, encoding='UTF-8')
        host = config.get(mysqlname, "host")
        user = config.get(mysqlname, "user")
        password = config.get(mysqlname, "password")
        db = config.get(mysqlname, "db")
        try:
            conn = pymysql.connect(host=host, user=user, password=password, database=db, charset='utf8',
                                   autocommit=True)
            return conn
        except Exception:
            print('mysql数据库连接异常')

    # 查询sql数据，并返回
    def selectwithparams(self, mysqlname, sql, params):
        # 获取游标
        cursor = MysqlDB().conn(mysqlname).cursor()
        try:
            count = cursor.execute(sql, params)
            if count == 1:
                result = cursor.fetchone()
                return result
            elif count > 1:
                result = cursor.fetchall()
                result2 = []
                for i in range(0, count):
                    result2.append(result[i][0])
                return result2
            elif count == 0:
                print(sql + '没有符合条件的查询数据')
                return None
        except:
            print(sql + '查询异常，清查看异常原因')
            traceback.print_exc()
        finally:
            cursor.close()
            MysqlDB().conn(mysqlname).close()

    def selectwithoutparams(self, mysqlname, sql):
        # 获取游标
        cursor = MysqlDB().conn(mysqlname).cursor()
        try:
            count = cursor.execute(sql)
            if count == 1:
                result = cursor.fetchone()
                return result
            elif count > 1:
                result = cursor.fetchall()
                result2 = []
                for i in range(0, count):
                    result2.append(result[i][0])
                return result2
            elif count == 0:
                result = 'null'
                print('无查询数据')
                return result
        except:
            print('查询异常，请查看异常原因')
            traceback.print_exc()
            return None
        finally:
            cursor.close()
            MysqlDB().conn(mysqlname).close()

    # insert、update、delete的sql数据
    def updatewithparams(self, mysqlname, sql, params):
        cursor = MysqlDB().conn(mysqlname).cursor()
        try:
            cursor.execute(sql, params)
            MysqlDB().conn(mysqlname).commit()
            # print(sql + ' 更新成功')
        except:
            print(sql + ' 更新异常')
        finally:
            cursor.close()
            MysqlDB().conn(mysqlname).close()

    # insert、update、delete的sql数据
    def updatewithoutparams(self, mysqlname, sql):
        cursor = MysqlDB().conn(mysqlname).cursor()
        try:
            cursor.execute(sql)
            MysqlDB().conn(mysqlname).commit()
            # print(sql + ' 更新成功')
        except:
            # print('执行sql，更新异常')
            print(sql + ' 更新异常')
        finally:
            cursor.close()
            MysqlDB().conn(mysqlname).close()

    def deletecustomer(self, mysqlname, tel):
        # 判断手机号是否已注册
        sql1 = 'select count(id) from app_user where tel= %s'
        count = MysqlDB().selectwithparams(mysqlname, sql1, tel)[0]
        if count == 0:
            print('手机号未注册')
        elif count > 0:
            print('手机号已注册，开始清理我方mysql库数据')
            cursor = MysqlDB().conn(mysqlname).cursor()
            with open(deletesqlpath, 'r', encoding='utf-8') as file:
                sql = file.readlines()
                file.close()
            for line in sql:
                line2 = str(line).replace('19900000000', tel)
                cursor.execute(line2)
                MysqlDB().conn(mysqlname).commit()
            time.sleep(1)
            selectsql = 'select count(*) from app_user where tel= %s'
            result = MysqlDB().selectwithparams(mysqlname, selectsql, tel)[0]
            if result == 0:
                print('清数工具执行成功')
            else:
                print('清数工具执行失败，请手动处理！')








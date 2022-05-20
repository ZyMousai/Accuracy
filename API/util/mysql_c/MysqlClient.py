# coding=utf-8
# -*- coding:utf-8 -*-
# @Author: zy
# @Date:   2022.5.20
# @Last Modified by:
# @Last Modified time:
"""单线程操作mysql"""
import pymysql


class MysqlClient(object):
    def __init__(self, host, port, database, user, password):
        """
        :param host:数据库ip地址
        :param port:数据库端口
        :param database:库名
        :param user:用户名
        :param password:密码
        """
        self._conn = pymysql.Connect(host=host, port=port, database=database, user=user, password=password)
        self._cursor = self._conn.cursor()

    def close(self):
        """关闭连接"""
        self._cursor.close()
        self._conn.close()

    def __execute(self, sql, param=()):
        """处理sql语句"""
        count = self._cursor.execute(sql, param)
        return count

    def select_one(self, sql, param=()):
        """
        查询单个结果
        :param sql: qsl语句
        :param param: sql参数
        :return: 结果数量和查询结果集
        """
        count = self.__execute(sql, param)
        result = self._cursor.fetchone()
        return count, result

    def select_many(self, sql, param=()):
        """
        查询多个结果
        :param sql: qsl语句
        :param param: sql参数
        :return: 结果数量和查询结果集
        """
        count = self.__execute(sql, param)
        result = self._cursor.fetchall()
        return count, result

    def handle_one(self, sql, param=()):
        """
        处理一条数据，增删改
        :param sql:
        :param param:
        :return:
        """
        try:
            self.__execute(sql, param)
            self._conn.commit()
            return True
        except Exception as e:
            self._conn.rollback()
            print('mysql handle_one fail >>>>' + str(e))
            return False

    def handle_many(self, sql, param=()):
        """
        处理多条数据，增删改
        :param sql:
        :param param:
        :return:
        """
        try:
            self._cursor.executemany(sql, param)
            self._conn.commit()
            return True
        except Exception as e:
            self._conn.rollback()
            print('mysql handle_many fail >>>>' + str(e))
            return False

    # def execute(self, sql, param=()):
    #     count = self.__execute(sql, param)
    #     return count

    def begin(self):
        """开启事务"""
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """结束事务"""
        if option == 'commit':
            self._conn.autocommit()
        else:
            self._conn.rollback()

# if __name__ == "__main__":
#     # 调用案例
#     mc = MysqlClient(log_obj)
#     # 查询单条
#     sql1 = 'SELECT * FROM netloan_2017_03_10_t3_1000  WHERE  id = 1'
#     result1 = mc.select_one(sql1)
#     if int(result1[0]) != 0:
#         print result1[1]
#
#     # 查询多条
#     sql2 = 'SELECT * FROM netloan_2017_03_10_t3_1000  WHERE  id IN (%s,%s,%s)'
#     param = (2, 3, 4)
#     result2 = mc.select_many(sql2)
#     if int(result2[0]) != 0:
#         print result2[1]
#
#     # 处理单条
#     sql3 = 'insert into config_servers (server_ip,server_username,' \
#            'server_password,server_type) value (%s,%s,%s,%s,%s)'
#     param = ('45.79.40.42', 'admin@hayd.com', '8cc9571c385bd3b784168dcdce986c49', 'ftp')
#     handle_result = mc.handle_one(sql3, param)
#     if handle_result:
#         pass
#     else:
#         pass
#     # 处理多条
#     params = [('45.79.40.42', 'admin@hayd.com', '8cc9571c385bd3b784168dcdce986c49', 'ftp'),
#               ('45.79.40.42', 'admin@hayd.com', '8cc9571c385bd3b784168dcdce986c49', 'ftp')]
#     handle_result = mc.handle_many(sql3, params)
#     if handle_result:
#         pass
#     else:
#         pass

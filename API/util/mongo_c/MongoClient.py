# -*- coding:utf-8 -*-
# @Author: zy
# @Date:   2020.11.16 17:36
# @Last Modified by: zy
# @Last Modified time: 2020.11.24.16:50

import pymongo


class MongoClient(object):

    def __init__(self, **kwargs):
        """
        :param host: 数据库ip地址
        :param port: 数据库端口
        :param username: 用户名
        :param password: 密码
        :param database: 库名
        对mongo的增删改查通用封装
        """
        self.__host = kwargs['host']
        self.__port = kwargs['port']
        self.__username = kwargs['username']
        self.__password = kwargs['password']
        self.__database = kwargs['db']
        self.__db = None
        self.page_size = 2
        self.page_number = 1
        self.max_page_size = 100
        # 认证
        # self.__db.authenticate(username, password)
        if not self.__db:
            self.__get_conn()

    def __get_conn(self):
        # # 连接
        # self.__client = pymongo.MongoClient(
        #     'mongodb://{}:{}@{}:{}/'.format(self.__username, self.__password, self.__host, self.__port))
        # # 连接库
        # self.__db = self.__client[self.__database]

        # 连接
        self.__client = pymongo.MongoClient(self.__host, self.__port, connect=False)
        # 连接库
        self.__db = self.__client[self.__database]
        # 认证
        self.__db.authenticate(self.__username, self.__password)

    def close(self):
        self.__client.close()

    def select(self, collection, **kwargs):
        """
        查询数据
        :param collection: 表名
        :param kwargs: 查询条件
        :return:
        """
        # 连接col
        _col = self.__db[collection]
        return [x for x in _col.find(kwargs, {'_id': 0})]

    def add_data(self, collection, data):
        """
        新增数据,单条或者多条
        :param collection: 表明
        :param data: 新增的数据
        :return:
        """
        # 连接col
        _col = self.__db[collection]
        if isinstance(data, dict):
            return _col.insert_one(data)
        elif isinstance(data, list):
            return _col.insert_many(data)
        else:
            raise TypeError('fun add_data >>>"data" cannot be  {}'.format(type(data)))

    def delete_data(self, collection, **kwargs):
        """
        删除数据
        :param collection: 表名
        :param kwargs: 删除条件
        :return: {u'ok': 1.0, u'n': 0}
        """
        _col = self.__db[collection]
        return _col.remove(kwargs)

    def update_data(self, collection, filters, data, is_one=True):
        """
        更新数据
        :param collection: 表名
        :param data: 更新的数据
        :param filters: 更新条件
        :param is_one: 是否更新单条
        :return:
        """
        # 连接col
        _col = self.__db[collection]
        if is_one:
            return _col.update_one(filters, data)
        else:
            return _col.update_many(filters, data)

    def select_page(self, collection, **kwargs):
        """
        分页条件查询数据
        :param collection: 表名
        :param kwargs: 查询条件
        :return:
        """
        # 连接col
        _col = self.__db[collection]
        limit_count = kwargs.pop('limit_count')
        skip_count = kwargs.pop('skip_count')
        return [x for x in _col.find(kwargs).limit(limit_count).skip(skip_count)]

    def select_count(self, collection, **kwargs):
        """
        统计集合的数据量
        可以条件查询后统计
        :param collection: 表名
        :param kwargs: 查询条件
        :return:
        """
        # 连接col
        return self.__db[collection].count_documents(kwargs)

    def select_by_page(self, collection, page_size=None, page_number=None, sort=None, **kwargs):
        """
        查询数据
        :param collection: 表名
        :param page_size: 每页多少数据
        :param page_number: 页数
        :param sort: 排序
        :param kwargs: 查询条件
        :return:
        """
        # 连接col
        if page_size is None:
            page_size = self.page_size
        else:
            page_size = int(page_size)
            if page_size > self.max_page_size:
                page_size = self.max_page_size

        if page_number is None:
            page_number = self.page_number
        else:
            page_number = int(page_number)

        _col = self.__db[collection]
        # counts
        counts = _col.count_documents(kwargs)
        # result data
        skip = page_size * (page_number - 1)
        if sort is None:
            results = [x for x in _col.find(kwargs).limit(page_size).skip(skip)]
        else:
            results = [x for x in _col.find(kwargs).sort(*sort).limit(page_size).skip(skip)]

        return {
            "total_count": counts,
            "results": results,
        }

    def select_aggregate(self, collection, query_filter, **kwargs):
        _col = self.__db[collection]
        return [x for x in _col.aggregate(query_filter)]

    def select_sort(self, collection, sort=None, **kwargs):
        _col = self.__db[collection]
        return [x for x in _col.find(kwargs).sort(*sort)]

# if __name__ == '__main__':
#     m = MongoClient()
#     import datetime
#
#     b = {"$match": {
#         "date_time": {"$gte": (datetime.datetime.now() + datetime.timedelta(days=-8)).strftime('%Y-%m-%d')},
#         "task_uuid": "91f68a2e-beb6-11eb-b79f-00e05c6800b0"}}
#     a = {"$group": {"_id": "$date_time", "total_count": {"$sum": '$click_count'}}}
#     c = {"$sort": {"_id": -1}}
#
#     print(m.select_aggregate("task_click_history",[b,a,c]))

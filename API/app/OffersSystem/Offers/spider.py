import random

import requests

from util.mysql_c.MysqlClient import MysqlClient


class UnionApi(object):
    def __init__(self, **account_info):
        # #### 账号信息分解
        self.__union_id = account_info['union_id']  # 联盟id
        self.__union_system_id = account_info['union_system_id']
        self.__union_system = account_info['union_system']
        self.__union_system_url = account_info['union_system_url']
        self.__account_id = account_info['account_id']
        self.__account = account_info['account']
        self.__account_password = account_info['account_password']
        self.__account_api_key = account_info['account_api_key']
        self.__account_options = account_info['account_options']
        self.__account_ip_info = account_info['account_ip_info']

        # #### 初始化参数
        # 请求连接
        self.__request_url = None
        # 请求代理
        self.__request_proxy = None
        # 请求参数
        self.__request_params = None

    def __request_union(self):
        self.__generate_requests_url()

        proxy = {
            ''
        }

        r = requests.get(url=self.__request_url)

    def __generate_requests_proxy(self):
        """
        请求代理
        :return:
        """
        """获取所有代理信息"""
        country = self.__account_ip_info['country']
        state = self.__account_ip_info['state']
        session_id = random.randint(10000, 99999)
        zone = 123  # todo
        password = 123
        if state:
            proxy = f'lum-customer-frankxiao-zone-{zone}-session-{session_id}-country-{country}-state-{state}:' \
                    f'{password}@zproxy.lum-superproxy.io:22225'
        else:
            proxy = f'lum-customer-frankxiao-zone-{zone}-session-{session_id}-country-{country}:' \
                    f'{password}@zproxy.lum-superproxy.io:22225'

        proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}

        self.__request_proxy = proxies

    def __generate_requests_url(self):
        """
        组建url
        :return:
        """
        # 选择domain
        request_url_choice = {
            'cake': self.__union_system_url.format(plate='Offers', fun='FeaturedOffer')
        }
        return request_url_choice[self.__union_system]

    def ____generate_requests_params(self):
        """
        请求参数
        :return:
        """
        pass

    def __parse_result(self):
        pass

    def run(self):
        # 1. 请求
        self.__request_union()
        #  2. 解析
        # self.__parse_result()

    def __del__(self):
        pass


class UnionApiDB(object):
    """数据库操作"""

    def __init__(self):
        # 初始化mysql连接
        self.__mysql = MysqlClient(host='45.63.5.115', port=3306, user='root', password='4242587f*',
                                   database='AccuracyDB')


class UnionApiRun(object):
    """流程类"""
    # 查询出相关信息
    # 发送请求解析数据
    # 入库


if __name__ == '__main__':
    system_t = {
        'hasoffers': 'https://{network-id}.api.hasoffers.com/Apiv3/json',  # 网盟id
        'offer18': 'https://api.offer18.com/api/{plate}/{fun}',  # 板块，功能
        'affise': 'http://api.adswapper.affise.com/{version}/{plate}',  # 版本，板块
        'everflow': 'https://api.eflow.team/{version}/{plate}/{fun}',  # 版本，板块，功能
        'cake': 'https://login.suited45.com/affiliates/api/{plate}/{fun}'  # 板块，功能
    }
    ttt = {
        'union_id': 1,
        'union_system_id': 5,
        'union_system': 'cake',
        'union_system_url': 'https://login.suited45.com/affiliates/api/{plate}/{fun}',
        'account_id': 1,
        'account': 'root',
        'account_password': '123',
        'account_api_key': '123',
        'account_options': {},
        'account_ip_info': {}

    }
    ax = UnionApi(**ttt)
    ax.run()

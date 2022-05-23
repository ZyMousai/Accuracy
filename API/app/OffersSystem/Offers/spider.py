import random

import requests
from concurrent.futures import ThreadPoolExecutor
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
        # 请求头
        self.__request_headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/99.0.4844.59 Mobile/15E148 Safari/604.1'
        }
        # 解析前的请求结果
        self.__response = None
        # 解析后的请求响应体
        self.parse_response = None

        # #### lum 代理信息
        # todo 暂时写死
        self.__customer = 'c_8497f263'
        self.__zone = 'mk_jjj'
        self.__password = '6az62t9nrgbi'

    def __request_union(self):
        # 组建url
        self.__generate_requests_url()
        # 组建params
        self.____generate_requests_params()
        # 组建代理
        self.__generate_requests_proxy()
        # 发送请求
        r = requests.get(url=self.__request_url, params=self.__request_params, headers=self.__request_headers,
                         proxies=self.__request_proxy, verify=False)
        if r.status_code == 200:
            self.__response = r.content
            r.close()

    def __generate_requests_proxy(self):
        """
        请求代理
        :return:
        """
        """获取所有代理信息"""
        country = self.__account_ip_info['country']
        state = self.__account_ip_info['state']
        session_id = random.randint(10000, 99999)
        if state:
            proxy = f'lum-customer-{self.__customer}-zone-{self.__zone}-session-{session_id}-country-{country}' \
                    f'-state-{state}:{self.__password}@zproxy.lum-superproxy.io:22225'
        else:
            proxy = f'lum-customer-{self.__customer}-zone-{self.__zone}-session-{session_id}-country-{country}:' \
                    f'{self.__password}@zproxy.lum-superproxy.io:22225'

        proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}

        self.__request_proxy = proxies

    def __generate_requests_url(self):
        """
        组建url
        :return:
        """
        # 选择domain
        # 目前访问得都是offers板块
        if self.__union_system == 'cake':
            self.__request_url = self.__union_system_url.format(plate='Offers', fun='FeaturedOffer')
        elif self.__union_system == 'hasoffers':
            self.__request_url = self.__union_system_url.format(network_id=self.__account_options['NetworkId'],
                                                                plate='Affiliate_Offer', fun='findAll')
        elif self.__union_system == 'offer18':
            self.__request_url = self.__union_system_url.format(plate='af', fun='offers')
        elif self.__union_system == 'affise':
            self.__request_url = self.__union_system_url.format(version='3.0', fun='offers')
        elif self.__union_system == 'everflow':
            self.__request_url = self.__union_system_url.format(version='v1', plate='affiliates', fun='alloffers')
        elif self.__union_system == 'adpump':
            pass
        elif self.__union_system == 'imp':
            pass
        else:
            pass

    def ____generate_requests_params(self):
        """
        请求参数
        :return:
        """
        if self.__union_system == 'hasoffers':
            self.__request_params = {
                'api_key': self.__account_api_key,
            }
        elif self.__union_system == 'offer18':
            self.__request_params = {
                'key': self.__account_api_key,
                'aid': self.__account_options['affiliate_id'],
                'mid': self.__account_options['mid']
            }
        elif self.__union_system == 'affise':
            self.__request_params = {}
            self.__request_headers['API-Key'] = self.__account_api_key
        elif self.__union_system == 'everflow':
            self.__request_params = {}
            self.__request_headers['X-Eflow-API-Key'] = self.__account_api_key
            self.__request_headers['content-type'] = 'application/json'
        elif self.__union_system == 'cake':
            self.__request_params = {
                'api_key': self.__account_api_key,
                'affiliate_id': self.__account_options['affiliate_id']
            }
        elif self.__union_system == 'adpump':
            pass
        elif self.__union_system == 'imp':
            pass
        else:
            pass

    def __parse_result(self):
        if self.__union_system == 'hasoffers':
            from app.OffersSystem.Offers.SpiderParse.HasOffers import HasOffersParse
            self.parse_response = HasOffersParse.parse(self.__union_id, self.__account_id, self.__response)
        elif self.__union_system == 'offer18':
            pass
        elif self.__union_system == 'affise':
            pass
        elif self.__union_system == 'everflow':
            pass
        elif self.__union_system == 'cake':
            pass
        elif self.__union_system == 'adpump':
            pass
        elif self.__union_system == 'imp':
            pass
        else:
            pass

    def run(self):
        # 1. 请求
        self.__request_union()
        #  2. 解析
        self.__parse_result()


class UnionApiDB(object):
    """数据库操作"""

    def __init__(self):
        # 初始化mysql连接
        self.__mysql = MysqlClient(host='45.63.5.115', port=3306, user='root', password='4242587f*',
                                   database='AccuracyDB')

    def get_accounts_info(self):
        sql = """select oa.id,oa.offers_account,oa.offers_pwd,oa.offers_api_key,oa.`options`,oa.ip_info,oa.union_id,
        ou.union_name,ou.union_url,ou.union_system_id,us.union_system,us.union_system_api_url from 
        (offers_account as oa LEFT JOIN offers_union as ou ON oa.union_id=ou.id) LEFT JOIN 
        union_system as us on us.id = ou.union_system_id where oa.status = 1;"""

        return self.__mysql.select_many(sql)

    def save_data(self, data):
        pass

    def close(self):
        self.__mysql.close()

    def __del__(self):
        self.close()


class UnionApiRun(object):
    """流程类"""

    @staticmethod
    def run():
        # 建立数据库链接
        mysql_conn = UnionApiDB()
        # 查询出相关信息
        query_info = mysql_conn.get_accounts_info()

        # 组建 任务相关信息
        task_list = []
        """
        oa.id,oa.offers_account,oa.offers_pwd,oa.offers_api_key,oa.`options`,oa.ip_info,oa.union_id,
        ou.union_name,ou.union_url,ou.union_system_id,us.union_system,us.union_system_api_url
        """
        for x in query_info[1]:
            task = {
                'union_id': x[6],
                'union_system_id': x[9],
                'union_system': x[10],
                'union_system_url': x[11],
                'account_id': x[0],
                'account': x[1],
                'account_password': x[2],
                'account_api_key': x[3],
                'account_options': x[4],
                'account_ip_info': x[5],

            }
            task_list.append(task)

        # 发送请求解析数据 使用线程池
        def run_union_api(task_info):
            ua_obj = UnionApi(**task_info)
            ua_obj.run()
            return ua_obj.parse_response

        executor = ThreadPoolExecutor(max_workers=5)

        result = [data for data in executor.map(run_union_api, task_list)]
        # 入库
        mysql_conn.save_data(result)
        # 关闭数据连接
        del mysql_conn


if __name__ == '__main__':
    system_t = {
        'hasoffers': 'https://{network_id}.api.hasoffers.com/Apiv3/json?Target={plate}&Method={fun}',  # 网盟id
        'offer18': 'https://api.offer18.com/api/{plate}/{fun}',  # 板块，功能
        'affise': 'http://api.adswapper.affise.com/{version}/{plate}',  # 版本，板块
        'everflow': 'https://api.eflow.team/{version}/{plate}/{fun}',  # 版本，板块，功能
        'cake': 'https://login.suited45.com/affiliates/api/{plate}/{fun}'  # 板块，功能
    }
    ttt = {
        'union_id': 5,
        'union_system_id': 4,
        'union_system': 'hasoffers',
        'union_system_url': 'https://{network_id}.api.hasoffers.com/Apiv3/json?Target={plate}&Method={fun}',
        'account_id': 5,
        'account': 'keisha@yourgreatchoice.com',
        'account_password': 'Adtrust123',
        'account_api_key': 'f2f1023c033d0ce3f46ed89d9c5ebde1f59c32935fd8558c2d672a141efcd000',
        'account_options': {
            "NetworkId": "adtrustmedia"
        },
        'account_ip_info': {
            "state": "MD",
            "country": "US"
        }

    }
    # ax = UnionApi(**ttt)
    # ax.run()
    # r = requests.get(url="https://adtrustmedia.api.hasoffers.com/Apiv3/json?Target=Affiliate_Offer&Method=findAll", params={"api_key":"f2f1023c033d0ce3f46ed89d9c5ebde1f59c32935fd8558c2d672a141efcd000"},
    #                  verify=False)
    # print(r.json())
    ax = UnionApiRun()
    ax.run()

import random
import datetime
import json
import requests
from concurrent.futures import ThreadPoolExecutor
from util.mysql_c.MysqlClient import MysqlClient

requests.packages.urllib3.disable_warnings()


class UnionApi(object):
    def __init__(self, **account_info):
        # 模块名
        self.__name = self.__class__.__name__
        # #### 账号信息分解
        self.__union_id = account_info['union_id']  # 联盟id
        self.__union_name = account_info['union_name']  # 联盟id
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
        # 解析前的请求结果 json格式
        self.__response_json_list = []
        # 解析前的请求结果 byte格式
        self.__response_content = None
        # 解析后的请求响应体
        self.parse_response = None
        # 请求page
        self.__page = 1
        # 请求pagesize
        self.__pagesize = 1000

        # #### lum 代理信息
        # todo 暂时写死
        self.__customer = 'c_8497f263'
        self.__zone = 'mk_jjj'
        self.__password = '6az62t9nrgbi'

    def __request_union(self):
        session = requests.Session()
        while True:
            # 组建url
            self.__generate_requests_url()
            # 组建params
            self.____generate_requests_params()
            # 组建代理
            self.__generate_requests_proxy()
            # 发送请求
            r = session.get(url=self.__request_url, params=self.__request_params, headers=self.__request_headers,
                            proxies=self.__request_proxy, verify=False)
            if r.status_code == 200:
                json_result = r.json()
                if self.__union_system == 'affise':
                    self.__response_json_list.append(json_result)
                    if json_result.get("pagination").get("next_page"):
                        self.__page = json_result.get("pagination").get("next_page")
                    else:
                        break
                elif self.__union_system == 'everflow':
                    if not json_result.get("offers"):
                        break
                    else:
                        self.__response_json_list.append(json_result)
                        if json_result.get("paging").get("total_count") > self.__pagesize:
                            self.__page += 1
                        else:
                            break
                else:
                    self.__response_json_list.append(json_result)
                    break

        session.close()

    def __generate_requests_proxy(self):
        """
        请求代理
        :return:
        """
        """获取所有代理信息"""
        country = self.__account_ip_info.get('country')
        state = self.__account_ip_info.get('state')
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
            self.__request_url = self.__union_system_url.format(plate='Offers', fun='Feed')
        elif self.__union_system == 'hasoffers':
            self.__request_url = self.__union_system_url.format(network_id=self.__account_options['NetworkId'],
                                                                plate='Affiliate_Offer', fun='findAll')
        elif self.__union_system == 'offer18':
            self.__request_url = self.__union_system_url.format(plate='af', fun='offers')
        elif self.__union_system == 'affise':
            self.__request_url = self.__union_system_url.format(version='3.0', plate='offers')
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
                'aid': self.__account_options['aid'],
                'mid': self.__account_options['mid']
            }
        elif self.__union_system == 'affise':
            self.__request_params = {
                'page': self.__page,
                'limit': self.__pagesize
            }
            self.__request_headers['API-Key'] = self.__account_api_key
        elif self.__union_system == 'everflow':
            self.__request_params = {
                "page": self.__page,
                "page_size": self.__pagesize
            }
            self.__request_headers['X-Eflow-API-Key'] = self.__account_api_key
            self.__request_headers['content-type'] = 'application/json'
        elif self.__union_system == 'cake':
            self.__request_params = {
                'api_key': self.__account_api_key,
                'affiliate_id': self.__account_options['affiliate_id'],
                "start_at_row": 1,
                "row_limit": self.__pagesize
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
            self.parse_response = HasOffersParse.parse(self.__union_id, self.__account_id, self.__response_json_list)
        elif self.__union_system == 'offer18':
            from app.OffersSystem.Offers.SpiderParse.Offer18Parse import Offer18Parse
            self.parse_response = Offer18Parse.parse(self.__union_id, self.__account_id, self.__response_json_list)
        elif self.__union_system == 'affise':
            from app.OffersSystem.Offers.SpiderParse.Affise import AffiseParse
            self.parse_response = AffiseParse.parse(self.__union_id, self.__account_id, self.__response_json_list)
        elif self.__union_system == 'everflow':
            from app.OffersSystem.Offers.SpiderParse.EverFlow import EverFlowParse
            self.parse_response = EverFlowParse.parse(self.__union_id, self.__account_id, self.__response_json_list)
        elif self.__union_system == 'cake':
            from app.OffersSystem.Offers.SpiderParse.CakeSystem import CakeSystemParse
            self.parse_response = CakeSystemParse.parse(self.__union_id, self.__account_id, self.__response_json_list)
        elif self.__union_system == 'adpump':
            pass
        elif self.__union_system == 'imp':
            pass
        else:
            pass

    def run(self):
        try:
            # 1. 请求
            self.__request_union()
            #  2. 解析
            self.__parse_result()
        except Exception as e:
            PrintLog.print_log(self.__name, PrintLog.ERROR,
                               f'Union:{self.__union_name}---UnionSystem:{self.__union_system}---'
                               f'Account:{self.__account}Url:{self.__request_url}---Page:{self.__page}---'
                               f'PageSize:{self.__pagesize}---Error:{str(e)}')
        else:
            PrintLog.print_log(self.__name, PrintLog.INFO,
                               f'Union:{self.__union_name}---UnionSystem:{self.__union_system}---'
                               f'Account:{self.__account}---Get Success')


class UnionApiDB(object):
    """数据库操作"""

    def __init__(self):
        # 模块名
        self.__name = self.__class__.__name__
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
        # 插入数据
        # sql = """insert into offers (is_delete,union_id,account_id,offers_name,offers_desc,pay,pay_unit,country,
        # offers_url) value (0,%s,%s,%s,%s,%s,%s,%s,%s)"""
        sql = """insert into offers (is_delete,union_id,account_id,offers_name,offers_desc,pay,pay_unit,country,
        offers_url) values """
        # insert_list = []
        if data:
            for offers in data:
                for offer in offers:
                    # 拼接sql 运行效率更快
                    offer_desc = offer['offers_desc']
                    offer_name = offer['offers_name']
                    if offer_desc:
                        offer_desc = offer_desc.replace('"', "'")
                    if offer_name:
                        offer_name = offer_name.replace('"', "'")
                    sql_p = f"""({0},{offer['union_id']},{offer['account_id']},"{offer_name}","{offer_desc}",{offer['pay']},"{offer['pay_unit']}","{offer['country']}","{offer['offers_url']}"),"""
                    sql += sql_p
                    # executemany 伪批量插入
                    # insert_list.append(
                    #     (
                    #         offer['union_id'],
                    #         offer['account_id'],
                    #         offer['offers_name'],
                    #         offer['offers_desc'],
                    #         offer['pay'],
                    #         offer['pay_unit'],
                    #         offer['country'],
                    #         offer['offers_url'],
                    #     )
                    # )
        sql = sql[:-1]
        tag = self.__mysql.execute_sql(sql)
        # tag = self.__mysql.handle_many(sql, insert_list, auto_commit=True)
        if not tag:
            raise SystemError('Save Data Failed.')

    def clear_table(self):
        # 清空表
        sql = """Delete from offers;"""
        # sql = """Truncate table offers;"""
        self.__mysql.handle_one(sql, auto_commit=False)

    def close(self):
        self.__mysql.close()

    def commit(self):
        self.__mysql.commit()

    def rollback(self):
        self.__mysql.rollback()

    def __del__(self):
        self.close()


class UnionApiRun(object):
    """流程类"""

    def __init__(self):
        # 模块名
        self.__name = self.__class__.__name__
        # 线程池数量
        self.__thread_num = 5

    def run(self):
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
        print_task_list = []
        for x in query_info[1]:
            task = {
                'union_id': x[6],
                'union_name': x[7],
                'union_system_id': x[9],
                'union_system': x[10],
                'union_system_url': x[11],
                'account_id': x[0],
                'account': x[1],
                'account_password': x[2],
                'account_api_key': x[3],
                'account_options': json.loads(x[4]),
                'account_ip_info': json.loads(x[5]),
            }
            task_list.append(task)
            print_task_list.append(
                {
                    'union_id': x[6],
                    'union_name': x[7],
                    'account_id': x[0],
                    'account': x[1],
                }
            )

        # 打印日志
        PrintLog.print_log(self.__name, PrintLog.INFO, f'ThreadNum:{self.__thread_num}---TotalTask:{print_task_list}')

        # 发送请求解析数据 使用线程池
        def run_union_api(task_info):
            ua_obj = UnionApi(**task_info)
            ua_obj.run()

            return ua_obj.parse_response

        # 开始执行
        executor = ThreadPoolExecutor(max_workers=self.__thread_num)
        result = [data for data in executor.map(run_union_api, task_list)]

        if result:
            # 清空现有表
            mysql_conn.clear_table()
            PrintLog.print_log(self.__name, PrintLog.INFO, 'TableName<offers> Clear Success')
            try:
                # 入库
                mysql_conn.save_data(result)
                PrintLog.print_log(self.__name, PrintLog.INFO, 'SaveData Success')

            except Exception as e:
                mysql_conn.rollback()
                PrintLog.print_log(self.__name, PrintLog.ERROR, f'SaveData Failed, Rollback Success,Error:{str(e)}')

        # 关闭线程池
        executor.shutdown()
        # 关闭数据连接
        del mysql_conn


class PrintLog(object):
    INFO = 'INFO'
    ERROR = 'ERROR'

    @staticmethod
    def print_log(system_name, log_level, message):
        now_time = str(datetime.datetime.now())
        log_format = f"{system_name}---{log_level}---{now_time}---{message}"
        print(log_format)


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
    ax = UnionApiRun()
    ax.run()

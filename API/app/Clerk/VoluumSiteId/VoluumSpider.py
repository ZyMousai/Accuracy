""" voluum spider入口"""

import requests
import datetime

from config import globals_config
from util.mongo_c.MongoClient import MongoClient


class VoluumSpider(object):
    key_id = "63646237-5169-4fad-bb01-bb372b45fe4d"
    key = "egfe60XJYIDVgBQmQCGTzQBelUvwfpzigtfb"
    base_url = "https://api.voluum.com"

    def __init__(self):
        self.token = ''
        self.post_h = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8'
        }

        self.get_h = {
            'Accept': 'application/json',
        }

    def get_token(self):
        """
        获取token和刷新token
        :return:
        """
        url = self.base_url + '/auth/access/session'
        p = {
            'accessId': self.key_id,
            'accessKey': self.key
        }

        r = requests.post(url, json=p, headers=self.post_h)

        if r.status_code == 200:
            self.token = r.json()['token']

            self.get_h['cwauth-token'] = self.token

            print(self.get_h)

    def get_campaign(self):
        url = self.base_url + '/campaign?includeDeleted=false'

        r = requests.get(url, headers=self.get_h)
        body = {'status_code': r.status_code}
        if r.status_code == 200:
            body['body'] = r.json()
        else:
            body['body'] = {}
        return body

    def get_reports(self):
        url = self.base_url + '/report'
        p = {
            'limit': 1000,
            'groupBy': 'campaign',
            'from': datetime.datetime.now().strftime("%Y-%m-%dT00:00:00Z"),
            'to': (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z"),
            'tz': 'America/New_York'
        }
        r = requests.get(url, params=p, headers=self.get_h)

        body = {'status_code': r.status_code}
        if r.status_code == 200:
            body['body'] = r.json()['rows']
        else:
            body['body'] = {}

        return body

    def get_one_reports(self, campaign_id):
        from_time = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%dT00:00:00Z")
        to_time = datetime.datetime.now().strftime("%Y-%m-%dT00:00:00Z")
        url = self.base_url + '/report' + f'?from={from_time}&to={to_time}&tz=America/New_York&conversionTimeMode=VISIT&currency=USD&sort=visits&direction=desc&column=customVariable2&column=assocId&column=visits&column=uniqueVisits&column=clicks&column=uniqueClicks&column=conversions&column=revenue&column=cost&column=costSources&column=profit&column=cpv&column=ictr&column=ctr&column=cr&column=cv&column=roi&column=epv&column=epc&column=ap&column=errors&column=rpm&column=ecpm&column=ecpc&column=ecpa&column=transitivePause&column=actions&column=type&column=readOnly&column=deleted&column=campaignType&column=isOptimizationEnabled&column=externalCampaignId&column=isDsp&groupBy=custom-variable-2&offset=0&limit=1000&include=ACTIVE&filter1=campaign&filter1Value={campaign_id}'

        r = requests.get(url, headers=self.get_h)

        body = {'status_code': r.status_code}
        if r.status_code == 200:
            body['body'] = r.json()['rows']
        else:
            body['body'] = {}

        return body


class VoluumData(VoluumSpider):
    """数据入库"""

    @staticmethod
    def __is_clear_database(mongo, clo_name):
        data_num = mongo.select_count(clo_name)
        if data_num > 0:
            mongo.delete_data(clo_name)

    def add_campaign(self):
        try:
            clo_name = 'voluum_campaigns'
            mongo = MongoClient(**globals_config.MONGO_INFO.__dict__)

            self.__is_clear_database(mongo, clo_name)

            self.get_token()
            body = self.get_campaign()
            mongo.add_data(clo_name, body['body']['campaigns'])
            mongo.close()
        except:
            pass
        print('**add_campaign OK')

    def add_reports(self):
        clo_name = 'voluum_reports'
        mongo = MongoClient(**globals_config.MONGO_INFO.__dict__)

        self.__is_clear_database(mongo, clo_name)

        self.get_token()
        body = self.get_reports()
        mongo.add_data(clo_name, body['body'])
        mongo.close()

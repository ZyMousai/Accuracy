import requests
import csv
from lxml import etree


class AdpumpParse():

    @staticmethod
    def parse(union_id, account_id, response_data):
        result = list()
        for i in response_data:
            html_data = i[-1]

            html = etree.HTML(html_data)
            a = html_data.split("<h4>Description:</h4>")[1]

            desc = a.split('<div style="margin-top: 20px; margin-bottom: 20px;">')[0]

            name = html.xpath('//*[@id="controller-wmOffers"]/div[1]/div[1]/article/div[2]/h1/text()')[0]

            pay_unit = html.xpath('//*[@id="wmOffers-aims-table"]/tr[2]/td[1]/small[1]/text()')[0].replace('Currency:',
                                                                                                           '').replace(
                '\n', '').replace('\t', '').strip()
            pay = html.xpath('//*[@id="wmOffers-aims-table"]/tr[2]/td[2]/text()')[0].replace('\n', '').replace(' ', '')

            result.append({
                "union_id": union_id,
                "account_id": account_id,
                "offers_name": name,
                "offer_id": i[0],
                "offers_desc": desc,
                "country": i[-2],
                "pay": pay,
                "pay_unit": str(pay_unit).replace("'",''),
                "offers_url": i[2],
                "remark": "",
            })
        return result

    # def offers_view_parse(self, url, proxies):
    #     req = requests.get(url, proxies=proxies, timeout=15)
    #     html = etree.HTML(req.text)
    #     a = req.text.split("<h4>Description:</h4>")[1]
    #
    #     desc = a.split('<div style="margin-top: 20px; margin-bottom: 20px;">')[0]
    #
    #     name = html.xpath('//*[@id="controller-wmOffers"]/div[1]/div[1]/article/div[2]/h1/text()')[0]
    #
    #     pay_unit = html.xpath('//*[@id="wmOffers-aims-table"]/tr[2]/td[1]/small[1]/text()')[0].replace('Currency:',
    #                                                                                                    '').replace(
    #         '\n', '').replace('\t', '').strip()
    #     pay = html.xpath('//*[@id="wmOffers-aims-table"]/tr[2]/td[2]/text()')[0].replace('\n', '').replace(' ', '')
    #
    #     offers_view_result = {
    #         "desc": desc,
    #         "name": name,
    #         "pay_unit": pay_unit,
    #         "pay": pay,
    #     }
    #     return offers_view_result

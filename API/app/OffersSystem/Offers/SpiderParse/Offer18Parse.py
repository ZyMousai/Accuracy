class Offer18Parse(object):

    @staticmethod
    def parse(union_id, account_id, data):
        result_list = []
        for x in data:
            response = x['data']
            for index, offer in response.items():
                result_list.append(
                    {
                        "offers_id": offer.get("offerid"),
                        "union_id": union_id,
                        "account_id": account_id,
                        "offers_name": offer["name"],
                        "offers_desc": offer["offer_terms"],
                        "country": offer["country_allow"],
                        "pay": offer["price"],
                        "pay_unit": offer["currency"],
                        "offers_url": offer["preview_url"].replace("\\", "")
                    }
                )

        return result_list


if __name__ == '__main__':
    tt = {
        "response": "200",
        "data": {
            "3060765": {
                "offerid": "3060765",
                "name": "LifeAfter (iPhone 8.0+, iPad 8.0+) JP - Non incent",
                "logo": "http:\/\/cpitraffic.com\/creative\/EbglMaIY8dzFG65iZkhzjvxdYXLW529r7uipWMx4",
                "status": "active",
                "category": "",
                "currency": "USD",
                "price": 0.603,
                "model": "CPA",
                "date_start": "2020-03-02 00:00:00",
                "date_end": "2020-10-16 11:07:23",
                "preview_url": "https:\/\/apps.apple.com\/US\/app\/id1441752845?ls=1&mt=8",
                "offer_terms": "You CAN T deliver to Music FM .*This is the MONTHLY TOTAL budget.*As for campaign name and delivery os , Please refer to this e-mail subject.*Payment can not be made when fraudulent outcome.*It is fraud that over 1 hour from clicks to installs. Restrictions :- Adult traffic -> Allow : false Incentivized traffic -> Allow : false Inappropriate sites -> Allow : false Illegal sites -> Allow : false Bot traffic -> Allow : false Misleading -> Allow : false ",
                "offer_kpi": "",
                "country_allow": "JP",
                "country_block": "",
                "city_allow": "",
                "city_block": "",
                "os_allow": "",
                "os_block": "",
                "device_allow": "",
                "device_block": "",
                "isp_allow": "",
                "isp_block": "",
                "capping_budget_period": "",
                "capping_budget": "",
                "capping_conversion_period": "",
                "capping_conversion": "",
                "click_url": "",
                "impression_url": "",
                "authorized": "false",
                "landing_pages": "",
                "creatives": "",
                "events": None
            }, }}
    Offer18Parse.parse(1, 2, tt)

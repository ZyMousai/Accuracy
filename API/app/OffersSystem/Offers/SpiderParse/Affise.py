class AffiseParse(object):

    @staticmethod
    def parse(union_id, account_id, data):
        result_list = []
        for x in data:
            response = x['offers']

            for offer in response:
                country = offer.get("countries")
                if country:
                    country = ",".join(country)
                else:
                    country = ",".join(offer["payments"][0]["countries"])
                result_dict = {
                    "offers_id": offer.get("id"),
                    "union_id": union_id,
                    "account_id": account_id,
                    "offers_name": offer["title"],
                    "country": country,
                    "pay": offer["payments"][0]["revenue"],
                    "pay_unit": offer["payments"][0]["currency"],
                    "offers_url": offer["preview_url"],
                    "offers_desc": None
                }
                for index, desc in offer["description_lang"].items():
                    if desc:
                        result_dict["offers_desc"] = desc
                        break
                result_list.append(result_dict)
        return result_list


if __name__ == '__main__':
    tt = {
        "status": 1,
        "offers": [{
            "id": 78,
            "offer_id": "78",
            "bundle_id": "",
            "title": "Sweepstakes Bucks (US) (non-incent)",
            "preview_url": "https://www.sweepstakesbucks.com",
            "description_lang": {
                "cn": "",
                "en": "<p>Requirements: Registration form submit Target: 18+ (The offer only converts for ages 18 and above)</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>**** Must pass website/app on click URL*****</p>",
                "es": "",
                "ka": "",
                "my": "",
                "pt": "",
                "ru": "",
                "vi": ""
            },
            "cr": 5.47,
            "epc": 0.1094,
            "affiliate_epc": 0.0766,
            "logo": "https://affise-media-service-prod.s3.eu-central-1.amazonaws.com/affise-media-service-prod/offers/4843/78/369099006.200x200.png",
            "logo_source": "https://affise-media-service-prod.s3.eu-central-1.amazonaws.com/affise-media-service-prod/offers/4843/78/369099006.200x200.png",
            "stop_at": "",
            "sources": [],
            "categories": [
                "direct",
                "survey / sweepstakes"
            ],
            "full_categories": [
                {
                    "id": "5f73ade7e56b7000402396e3",
                    "title": "direct"
                },
                {
                    "id": "5f73ade2e56b70004641d683",
                    "title": "survey / sweepstakes"
                }
            ],
            "payments": [
                {
                    "countries": [],
                    "cities": [],
                    "devices": [],
                    "os": [],
                    "goal": "1",
                    "revenue": 1.4,
                    "currency": "usd",
                    "title": "",
                    "type": "fixed",
                    "country_exclude": False
                }
            ],
            "caps": [
                {
                    "goals": {},
                    "period": "day",
                    "type": "conversions",
                    "value": 100,
                    "goal_type": "all",
                    "country_type": "all",
                    "country": []
                }
            ],
            "caps_status": [
                "confirmed",
                "declined"
            ],
            "required_approval": True,
            "strictly_country": 1,
            "strictly_os": None,
            "strictly_brands": [],
            "is_cpi": False,
            "creatives": [
                {
                    "file_name": "0be51fa47ffec648a155dfb450269b55.gif",
                    "width": 300,
                    "height": 250,
                    "size": "42.12 KB",
                    "type": "image/gif",
                    "url": "https://affise-media-service-prod.s3.eu-central-1.amazonaws.com/affise-media-service-prod/offers/4843/78/0be51fa47ffec648a155dfb450269b55.gif",
                    "id": "31e247c9-a41e-4520-abf0-579657c7e4ba",
                    "title": "0be51fa47ffec648a155dfb450269b55",
                    "assets": None
                },
                {
                    "file_name": "30054da658fb49e334ad83a70543e46b.gif",
                    "width": 700,
                    "height": 400,
                    "size": "95.19 KB",
                    "type": "image/gif",
                    "url": "https://affise-media-service-prod.s3.eu-central-1.amazonaws.com/affise-media-service-prod/offers/4843/78/30054da658fb49e334ad83a70543e46b.gif",
                    "id": "989edc76-423f-400a-bc6f-e2a8e1e9804a",
                    "title": "30054da658fb49e334ad83a70543e46b",
                    "assets": None
                },
                {
                    "file_name": "5cbde8b5af1a65272e990d2f6b04a8ca.png",
                    "width": 700,
                    "height": 400,
                    "size": "213.51 KB",
                    "type": "image/png",
                    "url": "https://affise-media-service-prod.s3.eu-central-1.amazonaws.com/affise-media-service-prod/offers/4843/78/5cbde8b5af1a65272e990d2f6b04a8ca.png",
                    "id": "eeae96b8-366c-47bc-b661-459e6299fecc",
                    "title": "5cbde8b5af1a65272e990d2f6b04a8ca",
                    "assets": None
                },
                {
                    "file_name": "419342cb346e45a133e6f0b96f5821ce.png",
                    "width": 300,
                    "height": 600,
                    "size": "149.62 KB",
                    "type": "image/png",
                    "url": "https://affise-media-service-prod.s3.eu-central-1.amazonaws.com/affise-media-service-prod/offers/4843/78/419342cb346e45a133e6f0b96f5821ce.png",
                    "id": "b5adbbcd-d303-4e01-aadb-a5f06daccd77",
                    "title": "419342cb346e45a133e6f0b96f5821ce",
                    "assets": None
                },
                {
                    "file_name": "4ddbb766e350aef5d656ab4a94836ca3.gif",
                    "width": 700,
                    "height": 400,
                    "size": "127.01 KB",
                    "type": "image/gif",
                    "url": "https://affise-media-service-prod.s3.eu-central-1.amazonaws.com/affise-media-service-prod/offers/4843/78/4ddbb766e350aef5d656ab4a94836ca3.gif",
                    "id": "f07460c5-6b9b-4c59-8da2-9a49613b3de8",
                    "title": "4ddbb766e350aef5d656ab4a94836ca3",
                    "assets": None
                },
                {
                    "file_name": "f5c3f21cd04a56c2b16367367d961da0.png",
                    "width": 300,
                    "height": 250,
                    "size": "66.08 KB",
                    "type": "image/png",
                    "url": "https://affise-media-service-prod.s3.eu-central-1.amazonaws.com/affise-media-service-prod/offers/4843/78/f5c3f21cd04a56c2b16367367d961da0.png",
                    "id": "db222ea9-bb24-4eea-8b31-4f4130e62aa9",
                    "title": "f5c3f21cd04a56c2b16367367d961da0",
                    "assets": None
                }
            ],
            "creatives_zip": None,
            "landings": [],
            "links": [],
            "macro_url": "&sub1={clickid}&sub2={pid}&sub3={subsource}&sub5={app_name}",
            "link": "",
            "use_https": True,
            "use_http": False,
            "hold_period": 0,
            "kpi": {
                "en": ""
            },
            "click_session": "7d",
            "minimal_click_session": "0s",
            "strictly_isp": [],
            "restriction_isp": [],
            "targeting": [
                {
                    "country": {
                        "allow": [
                            "US"
                        ],
                        "deny": []
                    },
                    "region": {
                        "allow": {},
                        "deny": {}
                    },
                    "city": {
                        "allow": {},
                        "deny": {}
                    },
                    "os": {
                        "allow": [],
                        "deny": []
                    },
                    "isp": {
                        "allow": {},
                        "deny": {}
                    },
                    "ip": {
                        "allow": [],
                        "deny": []
                    },
                    "browser": {
                        "allow": [],
                        "deny": []
                    },
                    "brand": {
                        "allow": [],
                        "deny": []
                    },
                    "device_type": [],
                    "connection": [],
                    "id": "00000000-0000-0000-0000-000000000000",
                    "zip": [],
                    "sub_regexps": [],
                    "block_proxy": True,
                    "sub": {
                        "allow": {},
                        "deny": {}
                    }
                }
            ],
            "consider_personal_targeting_only": False,
            "hosts_only": False,
            "countries": [
                "US"
            ],
            "uniq_ip_only": True,
            "reject_not_uniq_ip": 1,
            "sign_clicks_integration": "no_sign"
        }]
    }
    AffiseParse.parse(1, 2, tt)

class CakeSystemParse(object):

    @staticmethod
    def parse(union_id, account_id, data):
        result_list = []
        for x in data:
            response = x['data']

            for offer in response:
                if offer.get("allowed_countries"):
                    country = offer.get("allowed_countries")[0].get("country_code")
                else:
                    country = None
                result_list.append(
                    {
                        "union_id": union_id,
                        "account_id": account_id,
                        "offers_name": offer.get("offer_name"),
                        "offers_desc": offer.get("description"),
                        "country": country,
                        "pay": offer["price"],
                        "pay_unit": offer["currency_symbol"],
                        "offers_url": offer.get("preview_link")
                    }
                )
        return result_list


if __name__ == '__main__':
    tt = {
        "row_count": 28,
        "data": [
            {
                "offer_id": 4051,
                "offer_contract_id": 5099,
                "campaign_id": None,
                "offer_name": "Insure My Car v1042 Email - Internal Only",
                "vertical_name": "Insurance",
                "offer_status": {
                    "offer_status_id": 2,
                    "offer_status_name": "Public"
                },
                "price": 11,
                "currency_id": 1,
                "currency_symbol": "$",
                "price_converted": 11,
                "price_format_id": 1,
                "price_format": "CPA",
                "preview_link": "",
                "thumbnail_image_url": "",
                "description": "",
                "restrictions": "",
                "allowed_countries": [],
                "allowed_media_types": [],
                "expiration_date": None,
                "tags": [],
                "advertiser_extended_terms": "",
                "hidden": False,
                "date_created": "2022-05-18T05:27:13.32",
                "price_min": 11,
                "price_max": 11,
                "percentage_min": None,
                "percentage_max": None
            }, ]}
    CakeSystemParse.parse(1, 2, tt)

class HasOffersParse(object):

    @staticmethod
    def parse(union_id, account_id, data):
        result_list = []
        for x in data:
            response = x['response']['data']

            for index, offers in response.items():
                for o_index, offer in offers.items():
                    result_list.append(
                        {
                            "offers_id": offer.get("id"),
                            "union_id": union_id,
                            "account_id": account_id,
                            "offers_name": offer["name"],
                            "offers_desc": offer["description"],
                            "country": None,
                            "pay": offer["default_payout"],
                            "pay_unit": "$",
                            "offers_url": offer["preview_url"]
                        }
                    )

        return result_list


if __name__ == '__main__':
    tt = {
        "request": {
            "Target": "Affiliate_Offer",
            "Format": "json",
            "Service": "HasOffers",
            "Version": "2",
            "api_key": "f2f1023c033d0ce3f46ed89d9c5ebde1f59c32935fd8558c2d672a141efcd000",
            "Method": "findAll",
            "_": "1653289115891"
        },
        "response": {
            "status": 1,
            "httpStatus": 200,
            "data": {
                "832": {
                    "Offer": {
                        "id": "832",
                        "name": "**[INTERNAL ONLY]** Comprehensive Home Warranty - US (CPL)",
                        "description": "<b>Description: </b>Don’t Let Unexpected Home Repairs Take Over What Matters Most<br><br>\r\n<b>Traffic types: </b>Internal Email Only<br><br>\r\n<b>Converts On: </b>Single page submit<br><br>\r\n<b>Restrictions: </b>NO INCENTIVIZED, NO PRE-POPPING, No Network Rebrokering On Approval Only; no Blog; no SMS<br><br>\r\n<b>Other: </b>*All pubs must be approved before running*<br><br>\r\n",
                        "require_approval": "1",
                        "require_terms_and_conditions": 0,
                        "terms_and_conditions": None,
                        "preview_url": "https://comprehensivehomewarranty.com/?",
                        "currency": None}}}}}
    HasOffersParse.parse(1, 2, tt)

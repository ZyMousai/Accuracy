import requests
import time

login_url = "https://app.impact.com/secure/login.user"

campaign_all_url = "https://app.impact.com/secure/nositemesh/market/campaign/newAll.ihtml?_dc=1653285301181&q=&joinState=all&featuredBrands=&categories=&rstatus=&actions=&additional=&countries=&servicearea=&ads=&page=1&startIndex=0&pageSize=25&sortBy=launchDate&sortOrder=ASC&tableId=t4892"

campaign_info_url = "https://app.impact.com/secure/directory/campaignAjax.ihtml?c={}"


class ImpParse():

    @staticmethod
    def parse(union_id, account_id, json_data_list):
        result = list()
        for json_data in json_data_list:
            # campaign_data = ImpParse().campaign_parse(data["CampaignId"], proxies, auth)
            country = ",".join(json_data.get("campaigns_data").get('ShippingRegions'))
            pay = 0
            pay_unit = ''
            for i in json_data.get("campaigns_data").get("public_terms").get('PayoutTermsList'):
                # for i in i.get("PayoutTermsList"):
                if i["TrackerName"] == "Transfer":
                    pay = i.get('PayoutAmount', 0)
                    pay_unit = i.get("PayoutCurrency", "")
            result.append({
                "union_id": union_id,
                "account_id": account_id,
                "offers_name": json_data.get("Name"),
                "offer_id": json_data.get("Id"),
                "offers_desc": json_data.get("Description"),
                "country": country,
                "pay": pay,
                "pay_unit": pay_unit,
                "offers_url": json_data.get("LandingPageUrl"),
                "remark": "",
            })

        return result

    # def campaign_parse(self, campaign_id, proxies, auth):
    #
    #     url = f"https://api.impact.com/Mediapartners/IRyDs4JcaoaM1291437SjnkGSbL4X35oF1/Campaigns/{campaign_id}"
    #
    #     headers = {"Accept": "application/json"}
    #     try:
    #         r = requests.get(url, proxies=proxies, timeout=15, auth=auth, headers=headers)
    #         json_data = r.json()
    #         pt_data = self.campaign_publicTerms_parse(json_data["PublicTermsUri"], proxies, auth)
    #         result = {
    #             "country": ",".join(json_data.get('ShippingRegions')),
    #             "pay": pt_data["pay"],
    #             "pay_unit": pt_data["pay_unit"]
    #         }
    #     except:
    #         result = {
    #             "country": "",
    #             "pay": 0,
    #             "pay_unit": ""
    #         }
    #
    #     return result
    #
    # def campaign_publicTerms_parse(self, parm_url, proxies, auth):
    #     url = "https://api.impact.com" + parm_url
    #     headers = {"Accept": "application/json"}
    #     try:
    #         r = requests.get(url, proxies=proxies, timeout=15, auth=auth, headers=headers)
    #         data = r.json()
    #         for i in data.get("PayoutTermsList"):
    #             if i["TrackerName"] == "Transfer":
    #                 return {"pay": i.get('PayoutAmount'), "pay_unit": i.get("PayoutCurrency")}
    #     except:
    #         return {"pay": 0, "pay_unit": ""}


if __name__ == '__main__':
    '''
    Id": "356309",
      "Name": "B2C 300x50",
      "Description": "",
      "CampaignId": "5170",
      "CampaignName": "CurrencyFair",
      "Type": "BANNER",
      "TrackingLink": "https://currencyfair.g6ww.net/c/1291437/356309/5170",
      "LandingPageUrl": "https://www.currencyfair.com/",
      "AdvertiserId": "361247",
      "AdvertiserName": "CurrencyFair",
      "Code": "<a href=\"https://currencyfair.g6ww.net/c/1291437/356309/5170\" target=\"_top\" id=\"356309\"><img src=\"//a.impactradius-go.com/display-ad/5170-356309\" border=\"0\" alt=\"\" width=\"300\" height=\"50\"/><\/a><img height=\"0\" width=\"0\" src=\"https://currencyfair.g6ww.net/i/1291437/356309/5170\" style=\"position:absolute;visibility:hidden;\" border=\"0\" />",
      "IFrameCode": "<iframe id=\"iframe_212\" src=\"//a.impactradius-go.com/gen-ad-code/1291437/356309/5170/\" width=\"300\" height=\"50\" scrolling=\"no\" frameborder=\"0\" marginheight=\"0\" marginwidth=\"0\"><\/iframe>",
      "Width": "300",
      "Height": "50",
      "CreativeUrl": "//a.impactradius-go.com/display-ad/5170-356309",
      "Labels": "",
      "AllowDeepLinking": "true",
      "MobileReady": "false",
      "Language": "ENGLISH",
      "StartDate": "2017-03-27T23:54:30+08:00",
      "EndDate": "",
      "Season": "",
      "TopSeller": "false",
      "SubjectLines": "",
      "FromAddresses": "",
      "UnsubscribeLink": "",
      "DealId": "",
      "DealName": "",
      "DealDescription": "",
      "DealState": "",
      "DealType": "",
      "DealScope": "",
      "DealPublic": "",
      "DealProducts": [],
      "DealCategories": "",
      "DiscountType": "",
      "DiscountAmount": "",
      "DiscountCurrency": "",
      "DiscountPercent": "",
      "DiscountMaximumPercent": "",
      "DiscountPercentRangeStart": "",
      "DiscountPercentRangeEnd": "",
      "Gift": "",
      "RebateAmount": "",
      "RebateCurrency": "",
      "DealDefaultPromoCode": "",
      "MinimumPurchaseAmount": "",
      "MinimumPurchaseAmountCurrency": "",
      "MaximumSavingsAmount": "",
      "MaximumSavingsCurrency": "",
      "BogoBuyQuantity": "",
      "BogoBuyScope": "",
      "BogoBuyName": "",
      "BogoBuyImageUrl": "",
      "BogoGetQuantity": "",
      "BogoGetScope": "",
      "BogoGetDiscountType": "",
      "BogoGetName": "",
      "BogoGetImageUrl": "",
      "BogoGetDiscountAmount": "",
      "BogoGetDiscountCurrency": "",
      "BogoGetDiscountPercent": "",
      "PurchaseLimitQuantity": "",
      "DealStartDate": "",
      "DealEndDate": "",
      "DealDateCreated": "",
      "DealDateLastUpdated": "",
      "Uri": "/Mediapartners/IRyDs4JcaoaM1291437SjnkGSbL4X35oF1/Ads/356309"
    '''
    pass

class EverFlowParse(object):

    @staticmethod
    def parse(union_id, account_id, data):
        response = data['offers']
        result_list = []
        for offer in response:
            result_list.append(
                {
                    "union_id": union_id,
                    "account_id": account_id,
                    "offers_name": offer["name"],
                    "offers_desc": offer["terms_and_conditions"],
                    "country": None,
                    "pay": 0,
                    "pay_unit": offer["currency_id"],
                    "offers_url": offer["preview_url"]
                }
            )
        return result_list


if __name__ == '__main__':
    tt = {
        "offers": [
            {
                "network_offer_id": 7,
                "network_id": 393,
                "name": "College Allstar (A)",
                "thumbnail_url": "",
                "network_category_id": 4,
                "preview_url": "https://www.collegeallstar.com/collegefunnel/",
                "offer_status": "active",
                "currency_id": "USD",
                "caps_timezone_id": 80,
                "date_live_until": "",
                "html_description": "Let us help you find a school and you may qualify for financial aid\n\nYOU MUST SUBMIT YOUR SUBID FOR APPROVAL WITH EACH CREATIVE, FAILURE TO COMPLY WILL RESULT IN NON-PAYMENT\nCAN-SPAM COMPLIANCE REQUIREMENT: YOU MUST INCLUDE YOUR OWN UNSUB LINK AND OPT-OUT ADDRESS IN ADDITION TO THE ADVERTISER'S.\n\nGuidelines for ad placements:\n• The main guidelines are to make sure the EDU message is first. We can mention financial aid in the content of an email or display ad, but we need to lead with EDU. I.e. Earn your degree and you may qualify for financial aid. \n• Email “From” and “Subject” lines can use different verbiage, but CAN NOT use language that includes: Financial Aid/scholarships, Promised job opportunities or salary, “Career(s),” School brand names, or incentivized offers (free laptops or gift card) - Approved subject line examples are: Pursue your dream by earning your degree, Find the right college for your degree today, Get the education that fits your interests, Flexible degree programs for working professionals - Start Today.\n• No sense of urgency—we need to avoid words like notification, notice, limited time, funds are limited, etc. Anything that suggests that the user may ‘miss out’ on the opportunity. \n• The schools are also sensitive to superlatives like “top” schools or “best” programs.\n• Not Allowed: NO Incentivized, NO Classified Ads, NO SMS, NO Tradename Bidding, NO Co-Registration, NO Adult traffic\n\nCONVERSION POINT: Converts on the selection of a school and the successful submission of the lead\n\nTHIS OFFER PAYS NET60\n\nPhysical Address Must  be used Address: 700 SW 78th Ave, Suite 101, Plantation, FL 33324\n\nThe following persons/companies and their aliases are Blacklisted and NOT allowed to run our offers:\nYour Great Choice - Keisha Flanigan & Marie Murphy\nFinance Summit - Shane Langley & Arpna Bhalla\nTravelmindsets - Shane Langley & John Knoll\nAllFreeTrial - Dehua Wang as Nicholas Arden\nJun Ouyang as Derek Schyvinck\nMatthew Oldt/Flipline\nFree Samples Plan - Lisa Zhou & Tao Jiang",
                "is_using_explicit_terms_and_conditions": True,
                "terms_and_conditions": "YOU MUST SUBMIT YOUR SUBID FOR APPROVAL WITH EACH CREATIVE, FAILURE TO COMPLY WILL RESULT IN NON-PAYMENT\nCAN-SPAM COMPLIANCE REQUIREMENT: YOU MUST INCLUDE YOUR OWN UNSUB LINK AND OPT-OUT ADDRESS IN ADDITION TO THE ADVERTISER'S.\n\nGuidelines for ad placements:\n• The main guidelines are to make sure the EDU message is first. We can mention financial aid in the content of an email or display ad, but we need to lead with EDU. I.e. Earn your degree and you may qualify for financial aid. \n• Email “From” and “Subject” lines can use different verbiage, but CAN NOT use language that includes: Financial Aid/scholarships, Promised job opportunities or salary, “Career(s),” School brand names, or incentivized offers (free laptops or gift card) - Approved subject line examples are: Pursue your dream by earning your degree, Find the right college for your degree today, Get the education that fits your interests, Flexible degree programs for working professionals - Start Today.\n• No sense of urgency—we need to avoid words like notification, notice, limited time, funds are limited, etc. Anything that suggests that the user may ‘miss out’ on the opportunity. \n• The schools are also sensitive to superlatives like “top” schools or “best” programs.\n• Not Allowed: NO Incentivized, NO Classified Ads, NO SMS, NO Tradename Bidding, NO Co-Registration, NO Adult traffic\n\n\nTHIS OFFER PAYS NET60\n\nThe following persons/companies and their aliases are Blacklisted and NOT allowed to run our offers:\nYour Great Choice - Keisha Flanigan & Marie Murphy\nFinance Summit - Shane Langley & Arpna Bhalla\nTravelmindsets - Shane Langley & John Knoll\nAllFreeTrial - Dehua Wang as Nicholas Arden\nJun Ouyang as Derek Schyvinck\nMatthew Oldt/Flipline\nFree Samples Plan - Lisa Zhou & Tao Jiang\n\nCREATIVES AND LPs:\nAll Creatives and LPs MUST be sent into Netiquette Ads for Approval.\nAll EMAIL and Display Creatives for all NON-INCENT Offers require approval.\nINCENT Offers do not require Creative approvals.\nDO NOT start live Traffic until your Account Manager approves your Promotion Materials as unapproved materials will result in NON Payment.\n\nNO Incentivized Traffic (Unless Specified)\nNO Craigslist Traffic\nNO Backpage Traffic\nNO Blogger Traffic\nNO BlogSpot Traffic\nNO Adult Traffic - (Unless Specified)\nNO Trademark Infringement - (Search Traffic)\nNO Spam - (Must be CANSPAM compliant for Email Traffic)\nNO Copyrighted Materials Allowed\nNO Pirated Content\nNO Fake/Misleading Campaigns\nNO Spamming, Craigslist Baiting\nNO use of the word “Free” or implying the user has \"Won\"\nNO Forced Installs, No Malware, No Spyware\nNO Forced Clicks\nNO Fake Pop Unders or Overs\nNO Auto Redirects\nNO Bots\n\n***In the case of 3rd party Affiliate Traffic, you are also bound to observe and follow the terms and conditions under this contract.\n\nCHARGEBACK CUT OFF:\nChargebacks for the previous month's activity will be confirmed by the 15th of the following month EOD. If the 15th of the following month is a federal holiday or weekend, the next business day will be the extended deadline for chargebacks to be provided to the Publisher.\n\nIf any chargebacks are warranted, a Chargeback report will be emailed to you, unless there is direct fraud then a chargeback report does not need to be provided by your Account Manager or Point of Contact at Netiquette Ads.\n\nAll Chargebacks will be communicated via email. If any of the above terms are violated you will be blocked from this offer or have your account banned from the Network and forfeit any payments.\n\nEDUCATION OFFERS:\nDue to changes in the Education vertical and the strict regulations from the FTC and participating schools, Netiquette Ads can NO longer finalize final stats for EDU offers on a Net 30 basis. With Advertisers not being able to confirm on exact terms, Netiquette Ads cannot set specific final stat dates for any Education Offer on the Network.\n\nWe make best efforts to follow a guideline of Net 30, 45 or 60 but cannot guarantee specific dates.\n\nAll final stats for the previous month's traffic will be verified once we obtain the final report from the Advertiser. We will then process any returns and you will be emailed directly.\n\nWe will provide you with the following via Email:\nFinal Payable Lead Count.\nFinal Payable Revenue Amount.\nFinal Chargeback Lead Count.\nA chargeback report direct from the Advertiser with data point information that has been supplied to us by the Advertiser.",
                "is_force_terms_and_conditions": True,
                "visibility": "require_approval",
                "is_caps_enabled": False,
                "is_using_suppression_list": False,
                "suppression_list_id": 0,
                "network_tracking_domain_id": 963,
                "daily_conversion_cap": 0,
                "weekly_conversion_cap": 0,
                "monthly_conversion_cap": 0,
                "global_conversion_cap": 0,
                "daily_payout_cap": 0,
                "weekly_payout_cap": 0,
                "monthly_payout_cap": 0,
                "global_payout_cap": 0,
                "daily_click_cap": 0,
                "weekly_click_cap": 0,
                "monthly_click_cap": 0,
                "global_click_cap": 0,
                "tracking_url": "https://www.nettracx.com/5ZS8GM/BP658/",
                "app_identifier": "",
                "time_created": 1560354163,
                "time_saved": 1651581554,
                "is_description_plain_text": True,
                "is_use_direct_linking": False,
                "relationship": {
                    "offer_affiliate_status": "approved"
                },
                "impression_tracking_url": ""
            }]}
    EverFlowParse.parse(1, 2, tt)

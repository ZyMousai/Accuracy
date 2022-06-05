# import time
# from concurrent.futures import ThreadPoolExecutor
#
# a = [1, 2, 3]
#
#
# def pp(aa):
#     return aa + 1
#
#
# executor = ThreadPoolExecutor(max_workers=5)
# lists = [1, 2, 3, 4, 5, 7, 8, 9, 10]
# result = [data for data in executor.map(pp, lists)]
#
# print(result)


import pandas
import datacompy

a = [
    {"id": 0, "union_id": 1, "account_id": 2, "offers_name": 3},
    {"id": 1, "union_id": 2, "account_id": 3, "offers_name": 5},
    {"id": 2, "union_id": 5, "account_id": 6, "offers_name": 7}
]

b = [{'union_id': 4, 'account_id': 4, 'offers_name': 'Insure My Car v1042 Email - Internal Only',
      'offers_desc': '', 'country': None, 'pay': 11.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'LowerMyBills - Long Form - No Splash', 'offers_desc': '',
      'country': None, 'pay': 72.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'LowerMyBills - Short Form', 'offers_desc': '',
      'country': None, 'pay': 36.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'NEW RoofingCostGuide *By Approval Only*', 'offers_desc': '',
      'country': None, 'pay': 11.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'xxxa312', 'offers_desc': '',
      'country': None, 'pay': 80.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - DownPaymentSurvey - SC',
      'offers_desc': '7 days a week ', 'country': None, 'pay': 90.0, 'pay_unit': '$',
      'offers_url': 'https://downpaymentsurvey.com'},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - EnhancedRelief - SC',
      'offers_desc': 'Converts on full lead submit \n7 days a week ', 'country': 'US', 'pay': 40.0,
      'pay_unit': '$', 'offers_url': 'https://enhancedrelief.com'},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - EnhancedRelief - SC',
      'offers_desc': 'Converts on full lead submit \n7 days a week ', 'country': None, 'pay': 90.0,
      'pay_unit': '$', 'offers_url': 'https://enhancedrelief.com'},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - FedsCutRates - GHM', 'offers_desc': '',
      'country': None, 'pay': 40.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - GovHomePrograms - CRT', 'offers_desc': '',
      'country': None, 'pay': 35.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - GovHomePrograms - CRT', 'offers_desc': '',
      'country': None, 'pay': 100.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - HarpQuiz.com',
      'offers_desc': 'Converts on full lead submit \n7 days a week \n', 'country': None, 'pay': 30.0,
      'pay_unit': '$', 'offers_url': 'https://harpquiz.com'},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - HomeRoofingSurvey - GHM', 'offers_desc': '',
      'country': 'US', 'pay': 90.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - HomeWindowSurvey - GHM', 'offers_desc': '',
      'country': None, 'pay': 100.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - InsuranceSpecialists (AutoGo2) - MP',
      'offers_desc': '', 'country': 'US', 'pay': 10.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - InsuranceSpecialists (Life) - MP ',
      'offers_desc': '', 'country': None, 'pay': 10.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - InsuranceSpecialists (Life) - MP ',
      'offers_desc': '', 'country': None, 'pay': 90.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - InsuranceSpecialists (Med2) - MP', 'offers_desc': '',
      'country': 'US', 'pay': 11.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - InsuranceSpecialists (Med2) - MP', 'offers_desc': '',
      'country': 'US', 'pay': 90.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - QualifiedSolarSurvey - GHM', 'offers_desc': '',
      'country': None, 'pay': 0.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - QualifiedSolarSurvey - GHM', 'offers_desc': '',
      'country': None, 'pay': 100.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - Rent2OwnQualifier - SC', 'offers_desc': '',
      'country': None, 'pay': 5.0, 'pay_unit': '$', 'offers_url': ''},
     {'union_id': 4, 'account_id': 4, 'offers_name': 'V2FE - Rent2OwnQualifier - SC', 'offers_desc': '',
      'country': None, 'pay': None, 'pay_unit': '$', 'offers_url': ''}, {'union_id': 4, 'account_id': 4,
                                                                         'offers_name': 'zzzEXPIRED -  DO NOT USE - V2FE - InsuranceSpecialists (Car3) - MP',
                                                                         'offers_desc': 'Auto Insurance \nDoes not pay on uninsured consumers \n',
                                                                         'country': None, 'pay': 8.0,
                                                                         'pay_unit': '$',
                                                                         'offers_url': 'https://car3.insurancespecialists.com/'}]

df1 = pandas.DataFrame(a)
df2 = pandas.DataFrame(b)
print(list(df2.loc[:, "pay"]))
# compare = datacompy.Compare(df1, df2, join_columns=['union_id', 'account_id', 'offers_name'])
# print(df1)
# print(df2)
#
# print("df1独有的行：")  # 输出第一个DF中有的，第二个没有记录
# print(compare.df1_unq_rows)
# print("df2独有的行：")  # 输出第二个DF中有的，第一个没有的记录
# print(compare.df2_unq_rows)

# delete_ids = list(compare.df1_unq_rows.loc[:, "id"])
# delete_ids = list(map(lambda x: int(x), delete_ids))
# print(delete_ids)


# print(compare.df2_unq_rows)
a = (10,)
print(str(a))

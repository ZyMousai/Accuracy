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


a = {
    1: {
        2: {
            3: {
                4: "5"
            }
        }
    }
}

for x, v in a.items():
    for xx, vv in v.items():
        for xxx, vvv in vv.items():
            print(vvv)

# coding: utf8
# @Author  : WangYe
# @contact : bigjeffwang@163.com
# @Time    : 2018/3/14 上午11:22
# @File    : test1

name_detail = {
    "2018-09-01": {
        "a": "1"
    },
    "2018-09-03": {
        "a": "3"
    },
    "2018-09-02": {
        "a": "2"
    },
    "2018-09-04": {
        "a": "4"
    },
}

keys = list(name_detail.keys())
keys.sort()
name_detail_list = [name_detail[key] for key in keys]



from apps.utils.util import get_format_day

a = "2018-1-1"
a1 = "2018-01-1"
a2 = "2018-01-01"

print(get_format_day(a))
print(get_format_day(a1))
print(get_format_day(a2))

import time
print(time.localtime())
print(str(time.time()).split(".")[0])



if 1 <= 2 <= 3: print(1)

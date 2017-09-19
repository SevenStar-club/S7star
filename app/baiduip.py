#!/usr/bin/env python
# coding=utf-8

"""
Function: BaiDuIP地址定位
Author:   endness
Time:     2016年10月20日 20:17:33
"""
import requests
import json
from pprint import *


ak = 'SGGZrM4LGtS79Lepjm4fyG02QxXdNGiM'
#IP为空默认本机IP
def search():
    url = "https://api.map.baidu.com/location/ip?ak=fyQhDwa0rxKCY9Z6nrr1CNqBvionXTce&coor=bd09ll"
    html = requests.get(url).content
    s = json.loads(html)
    pprint(s)
    data={}
    data["lng"] = s["content"]["point"]["x"]#经度
    data["lat"] = s["content"]["point"]["y"] #纬度
    data["formatted_address"] = s["content"]["address"] #详细地址
    # data["admin_area_code"] = s["content"]["address_component"]["admin_area_code"]#行政区划代码（身份证前6位）
    data["map"] = getmap(data["lng"],data["lat"])
    pprint(data)
    return data

def getmap(lng,lat):
    url = "http://api.map.baidu.com/staticimage?width=600&height=400&center=%s,%s&zoom=11"%(lng,lat)
    return url

if __name__ == "__main__":
    search()
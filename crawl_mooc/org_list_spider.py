#!/usr/bin/env python3
"""
@file: org_list_spider.py
@brief: 爬取中国大学MOOC机构url列表
@author: feihu1996.cn
@date: 18-08-28
@version: 1.0
"""

import re
import sys
from urllib.parse import urljoin
import threading, queue
import time, random

import requests
from lxml import etree
import redis

import config


pool = redis.ConnectionPool(host=config.redis_host, port=config.redis_port)
db_redis = redis.Redis(connection_pool=pool, encoding='utf-8')


def get_org_list():
    # 机构列表页
    org_list_url = "https://www.icourse163.org/university/view/all.htm#/"
    org_list_res = etree.HTML(requests.get(org_list_url).text)

    org_list = []

    org_name_pattern = "//a[@class='u-usity f-fl']/img/@alt"
    org_names = org_list_res.xpath(org_name_pattern)
    org_url_pattern = "//a[@class='u-usity f-fl']/@href"
    org_urls = org_list_res.xpath(org_url_pattern)
    org_urls = [urljoin("https://www.icourse163.org", item) for item in org_urls]


    for i in range(0, len(org_names)):
        org_list.append({
            "org_name": org_names[i],
            "org_url": org_urls[i]
        })

    return org_list


if __name__ == "__main__":
    org_list = get_org_list()
    
    # org_list = [org_list[random.randint(0, (len(org_list)-1))]]
    
    [db_redis.lpush("org_list", item) for item in org_list]
    print(len(org_list))


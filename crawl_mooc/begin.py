#!/usr/bin/env python3
"""
@file: begin.py
@brief: 中国大学MOOC网站整站爬取
@author: feihu1996.cn
@date: 18-08-28
@version: 1.0
"""

import re
import sys
from urllib.parse import urljoin
import threading, queue
import time, random
import json

import requests
from lxml import etree
import redis

import config

from course_org_spider import crawl_course_org
from course_teacher_spider import crawl_course_teacher
from course_spider import crawl_course

pool = redis.ConnectionPool(host=config.redis_host, port=config.redis_port)
db_redis = redis.Redis(connection_pool=pool, encoding='utf-8')

"""
for i in range(0, len(org_list)):
    if "武汉理工大学" == org_list[i]["org_name"]:
        print(i)
"""

# 爬取课程机构详情
"""
for item in org_list:
    org_url = item["org_url"]
    org_name = item["org_name"]

    print("开始爬取课程机构详情...")
    crawl_course_org(org_url=org_url, org_name=org_name)
"""

# item = eval(db_redis.lindex("org_list", int(input("请指定索引值："))).decode("utf8"))
# item = eval(db_redis.lindex("org_list", int(sys.argv[1])).decode("utf8"))
item = eval(db_redis.lpop("org_list").decode("utf8"))

# 爬取机构教师
# crawl_course_teacher(org_url=item["org_url"], org_name=item["org_name"])

crawl_course(org_url=item["org_url"], org_name=item["org_name"])


#!/usr/bin/env python3

"""
@file: banner_spider.py
@brief: 爬取首页轮播图
@author: feihu1996.cn
@date: 18-08-31
@version: 1.0
"""

import urllib.request
from urllib.parse import urljoin
import random
import datetime
import re
import time
import sys
import traceback
import logging
import queue
import threading

import requests
import pymysql
from selenium import webdriver
from lxml import etree
import pymysql
import redis

import config

host = config.host
port = config.port
database = config.database
user = config.user
db_password = config.password
charset = config.charset

headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
opener=urllib.request.build_opener()
opener.addheaders=[headers]

logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='spider.log',  
                    filemode='a') 

pool = redis.ConnectionPool(host=config.redis_host, port=config.redis_port)
db_redis = redis.Redis(connection_pool=pool, encoding='utf-8')

# 打开浏览器
browser = webdriver.Chrome()

# 获取首页数据
index_url = "https://www.icourse163.org/"
browser.get(index_url)
time.sleep(2)
data = browser.page_source
treedata = etree.HTML(data)

banner_xpath = '//div[@id="j-slideTop-slideBox"]/div[@class="ux-slider-carousel test"]/div[@class="ux-slider-carousel-items"]/div[@data-cate="轮播图"]'

banners = treedata.xpath(banner_xpath)
banner_titles = [
    "有用又有趣的经济学思维",
    "北大还是清华",
    "听作家讲写作",
    "中国饮食文化",
    "中国大学先修课",
    "玩游戏，学编程"
]

print("当前队列长度为:", len(banners))

for i in range(0, len(banners)):
    banner = banners[i]
    print("正在抓取轮播图", banner)
    
    # 标题
    title = banner_titles[i]
    print("title:", title)
    
    # 图片
    cover_image_xpath = 'a[@class="ux-slider-carousel-item-img-wrapper"]/img/@src'
    cover_image = "resource/images/banner_cover/2018/08/"
    cover_image_path = "/mnt/usb/public/source/project/qinXueOnLine/media/"
    cover_image_source = ''.join(banner.xpath(cover_image_xpath))
    if not cover_image_source.startswith(('http', 'https')):
        cover_image_source = "https://edu-image.nosdn.127.net/0bfc4f49-d107-4200-9abf-95451eff6c9c.jpg?imageView&quality=100"
    cover_suffix = re.compile("jpg|png", re.I).findall(cover_image_source)[0] if re.compile("jpg|png", re.I).findall(cover_image_source) else "jpeg"
    cover_image = cover_image + str(int(time.time())+i) + "." + cover_suffix
    filename = cover_image_path + cover_image
    urllib.request.urlretrieve(cover_image_source, filename=filename)
    print("cover_image:", cover_image)

    # 链接
    target_url_xpath = 'a/@href'
    target_url = ''.join(banner.xpath(target_url_xpath))
    print("target_url:", target_url)

    # 索引
    index = i
    print("index:", index)

    # 添加时间
    add_time = datetime.datetime.now().strftime("%Y-%m-%d")
    print("add_time:", add_time)
    
    # 写入数据库
    conn = pymysql.connect(host=host, port=port, user=user, password=db_password, db=database,charset=charset, cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        insert_sql = """
        INSERT INTO users_banner
                (
                title,
                cover_image,
                target_url,
                `index`,
                add_time
                )
        VALUES  (
                '{title}',
                '{cover_image}',
                '{target_url}',
                 {index},
                 '{add_time}'
                )
        """.format(
            title = title,
            cover_image = cover_image,
            target_url = target_url,
            index = index,
            add_time = add_time
        )
        print("正在执行sql:",insert_sql)
        cursor.execute(insert_sql)
        conn.commit()
   
    conn.close()

# 关闭浏览器
browser.quit()


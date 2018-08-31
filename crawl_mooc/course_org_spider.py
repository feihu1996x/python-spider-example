#!/usr/bin/env python3
"""
@file: course_org_spider.py
@brief: 课程机构爬虫
@author: feihu1996.cn
@date: 18-08-28
@version: 1.0
"""

import re
import sys
import random
import time
import urllib.request
from urllib.parse import urljoin
import datetime

import requests
import pymysql
from pymysql.cursors import DictCursor
from lxml import etree

import config


def crawl_course_org(org_url=None, org_name=None):
    print("正在爬取:"+ org_name + "," + org_url + "...")
    if "Y" != input("确定要继续吗?Y/N:"):
        sys.exit(1)

    host = config.host
    port = config.port
    database = config.database
    user = config.user
    password = config.password
    charset = config.charset

    headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
    opener=urllib.request.build_opener()
    opener.addheaders=[headers]

    # 机构首页
    # org_url = input("请输入机构首页:")
    print("org_url:" + org_url)

    # 学习人数
    print("正在获取学习人数...")
    student_num = random.randint(100, 10000)
    print("student_num:" + str(student_num))

    # 课程数
    print("正在获取课程数...")
    course_num = random.randint(1, 100)
    print("course_num:" + str(course_num))

    # 机构类别
    org_type = input("请输入机构类别(回车将使用默认值'高校')：") or "高校" 
    print("org_type：" + org_type)

    # 机构名称
    print("正在获取机构名称...")
    r = requests.get(org_url)
    org_name = ""
    org_name_pattern = re.compile('<div class="g-mn1c m-cnt">.*?<h1>(.*?)</h1>', re.S)
    org_name = org_name_pattern.findall(r.text)[0]
    # org_name = re.sub(r'[\?\s\xa0\u3000\u2002]+', '', org_name)
    org_name = org_name.strip()
    print("org_name:" + org_name)

    # 机构描述
    print("正在获取机构详情...")
    org_desc = ""
    org_desc_pattern = re.compile('<p class="f-f1 f-fc6">(.*?)</p>', re.S)
    org_desc = org_desc_pattern.findall(r.text)[0]
    org_desc = re.sub(r'[\?\s\xa0\u3000\u2002]+', '', org_desc)
    print("org_desc:" + org_desc)

    # 点击数
    print("正在获取点击数...")
    click_num = random.randint(100, 10000)
    print("click_num:" + str(click_num))

    # 收藏数
    print("正在获取收藏数...")
    fav_num = random.randint(100, 10000)
    print("fav_num:" + str(fav_num))

    # 封面图
    print("正在获取封面图...")
    org_cover = ""
    org_list_url = "https://www.icourse163.org/university/view/all.htm#/"
    r1 = requests.get(org_list_url)
    org_cover_pattern = "//a[@class='u-usity f-fl']/img[@alt='{org_name}']/@src".format(org_name=org_name)
    org_cover_source = etree.HTML(r1.text).xpath(org_cover_pattern)[0]
    org_cover_path = "/mnt/usb/public/source/project/qinXueOnLine/media/"
    org_cover_suffix = re.compile("(png|jpg)").findall(org_cover_source)[0] if re.compile("(png|jpg)").findall(org_cover_source) else "jpeg"
    org_cover = "resource/images/org_cover/2018/08/" + str(int(time.time())) + "." + org_cover_suffix
    urllib.request.urlretrieve(org_cover_source, filename=org_cover_path+org_cover)
    print("org_cover:" + org_cover)

    # 机构地址
    print("正在获取机构地址...")
    org_address_search = requests.get("https://www.baidu.com/s?ie=utf-8&wd={org_name}%20地址".format(org_name=org_name), headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'})
    org_address_source = re.sub(r'[\?\s\xa0\u3000\u2002]+', '', org_address_search.text)
    org_address_pattern = re.compile("地址[:：]{1}(.+?)</.*?>", re.S)
    if org_address_pattern.findall(org_address_source):
        print("org_address:" + org_address_pattern.findall(org_address_source)[0])
        if "Y" == input("确定继续吗?Y/N:"):
            org_address = org_address_pattern.findall(org_address_source)[0]
        else:
            org_address = input("请手动输入机构地址:")
            print("org_address:" + org_address)
    else:
        org_address = input("请手动输入机构地址:")
        print("org_address:" + org_address)

    # 所在城市(外键)
    print("正在获取所在城市...")
    org_city_patten = re.compile("[省]?(.*?)市", re.S)
    if org_city_patten.findall(org_address):
        print("org_city:" + org_city_patten.findall(org_address)[0])
        if "Y" == input("确定继续吗?Y/N:"):
            org_city = org_city_patten.findall(org_address)[0]
        else:
            org_city = input("请手动输入所在城市:")
            print("org_city:" + org_city)
    else:
        org_city = input("请手动输入所在城市:")
        print("org_city:" + org_city)
        
    insert_courseorg_sql = "INSERT INTO organizations_courseorg(org_name, org_desc, click_nums, fav_nums, cover_image, org_address, add_time, city_id, category, course_nums, student_nums, tag) VALUES('{org_name}', '{org_desc}', {click_nums}, {fav_nums}, '{cover_image}', '{org_address}', '{add_time}', {city_id}, '{category}', {course_nums}, {student_nums}, '{tag}')"
    insert_city_sql = "INSERT INTO organizations_city(city_name, add_time, city_desc) VALUES('{city_name}', '{add_time}', '{city_desc}')".format(city_name=org_city, add_time=datetime.datetime.now().strftime("%Y-%m-%d"), city_desc=org_city)
    query_city_sql = "SELECT id FROM organizations_city WHERE city_name='{city_name}'".format(city_name=org_city)
    confirm_courseorg_sql = "SELECT * FROM organizations_courseorg WHERE org_name='{org_name}'".format(org_name=org_name)

    conn = pymysql.connect(host=host, port=port, user=user, password=password, db=database, charset=charset, cursorclass=DictCursor)
    try:
        with conn.cursor() as cursor:
            print("正在执行sql:"+query_city_sql)
            if "Y" != input("确定继续吗? Y/N:"):
                sys.exit(1) 
            cursor.execute(query_city_sql)
            data_list = cursor.fetchall()
            if data_list:
                city_id = int(data_list[0]["id"])
            else:
                print("正在执行sql:" + insert_city_sql)
                if "Y" != input("确定继续吗? Y/N:"):
                    sys.exit(1) 
                cursor.execute(insert_city_sql)
                conn.commit()
                print("正在执行sql:" + query_city_sql)
                if "Y" != input("确定继续吗? Y/N:"):
                    sys.exit(1)
                cursor.execute(query_city_sql)
                data_list = cursor.fetchall()  
                city_id = int(data_list[0]["id"])  
                
            print("city_id:" + str(city_id)) 

            insert_courseorg_sql = insert_courseorg_sql.format(
                org_name = org_name,
                org_desc = org_desc,
                click_nums = click_num,
                fav_nums = fav_num,
                cover_image = org_cover,
                org_address = org_address,
                add_time = datetime.datetime.now().strftime("%Y-%m-%d"),
                city_id = city_id,
                category = org_type,
                course_nums = course_num,
                student_nums = student_num,
                tag = "万事皆空"
            )

            print("正在执行sql:" + insert_courseorg_sql)
            if "Y" != input("确定继续吗? Y/N:"):
                sys.exit(1) 
            cursor.execute(insert_courseorg_sql)
            conn.commit()
            print("正在执行sql:" + confirm_courseorg_sql)
            if "Y" != input("确定继续吗? Y/N:"):
                sys.exit(1) 
            cursor.execute(confirm_courseorg_sql)
            data_list = cursor.fetchall()
            if data_list:
                for data in data_list:
                   for k,v in data.items():
                        print(k + ":" + str(v)) 
    except Exception as e:
        print("sql执行异常:", e)
        conn.rollback()
    finally:
        conn.close()


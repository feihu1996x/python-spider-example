#!/usr/bin/env python3

"""
@file: course_teacher_spider.py
@brief: 爬取课程机构教师
@author: feihu1996.cn
@date: 18-08-28
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

import requests
import pymysql
from selenium import webdriver
from lxml import etree
import pymysql

import config
from worker import Worker

host = config.host
port = config.port
database = config.database
user = config.user
password = config.password
charset = config.charset

headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
opener=urllib.request.build_opener()
opener.addheaders=[headers]

logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='spider.log',  
                    filemode='a') 

def crawl_course_teacher(org_url=None, org_name=None):
    """
    爬取课程机构教师
    """

    print("正在爬取:%s" % org_name)

    points_list = [
        "教师讲课深入浅出，条理清楚，层层剖析，环环相扣，论证严密，结构严谨，用思维的逻辑力量吸引学生的注意力，用理智控制课堂教学过程",
        "教师讲课亲切自然，朴素无华，没有矫揉造作，也不刻意渲染，而是娓娓道来，细细诱导，师生在一种平等、协作、和谐的气氛下，进行默默的双向交流，将对知识的渴求和探索融于简朴、真实的情景之中，学生在静静地思考、默然地首肯中获得知识",
        "教师讲课情绪饱满，把对科学文化的热爱和追求融于对学生的关爱和期望之中，充满着对人的高度尊重和依赖",
        "教师讲课生动形象，机智诙谐，妙语连珠，动人心弦",
        "教师精于教学的技巧，充满机智，各种教学方法技巧可信手拈来，运用自如，恰到好处"
    ]
    
    # 打开浏览器    
    browser = webdriver.Chrome()
    
    # 访问机构首页
    browser.get(org_url)

    # 自动翻页
    i = 0
    while True:
        try:
            data = browser.page_source
            treedata = etree.HTML(data)
            teacher_url_xpath = "//div[@class='j-list f-cb']/div/a/@href|//div[@class='j-list f-cb']/a/@href"

            teacher_urls = [urljoin(org_url, item) for item in treedata.xpath(teacher_url_xpath) if re.sub(r'[\?\s\xa0\u3000\u2002]+', '', item)]

            def func(teacher_url, **kwargs):
                sub_browser = webdriver.Chrome()
                sub_browser.get(teacher_url)
                teacher_data = sub_browser.page_source
                tree_teacher_data = etree.HTML(teacher_data)

                # 获取所属机构
                course_org_id = 0
                # 获取姓名
                name = [re.sub(r'[\?\s\xa0\u3000\u2002\ufeff]+', '', item) for item in tree_teacher_data.xpath('//div[@class="u-ti-name"]/descendant-or-self::*/text()')]
                name = [item for item in name if item]
                name = name[0].strip() if name else ""
                print("name:" + name)
                # 获取工作年限
                working_years = random.randint(5,30)
                print("working_years:" + str(working_years))
                # 获取就职公司
                working_company = tree_teacher_data.xpath("//div[@class='u-ti-name']/span[@class='f-thide u-ti-name_span32']/a/text()")
                working_company = working_company[0].strip() if working_company else ""
                print("working_company:" + working_company)
                # 获取公司职位
                working_position = tree_teacher_data.xpath("//div[@class='u-ti-name']/span[@class='f-thide u-ti-name_span32']/span[@class='tag']/text()") 
                working_position = working_position[0].strip() if working_position else ""
                print("working_position:" + working_position)
                # 获取教学特点
                points = random.choice(points_list)
                print("points:" + points)
                # 获取点击数
                click_nums = random.randint(100,10000)
                print("click_nums:" + str(click_nums))
                # 获取收藏数
                fav_nums = random.randint(100, 10000)
                print("fav_nums:" + str(fav_nums))
                # 获取添加时间
                add_time = datetime.datetime.now().strftime("%Y-%m-%d")
                print("add_time:" + add_time)
                # 获取讲师头像
                head_shot = "resource/images/head_shot/2018/08/"
                head_shot_path = "/mnt/usb/public/source/project/qinXueOnLine/media/"
                head_shot_source = tree_teacher_data.xpath('//div[@class="u-ti-img  user-head e-hover-source"]/img/@src')[0] 
                if not head_shot_source.startswith(('http', 'https')):
                    head_shot_source = "http://www.feihu1996.cn/img/logo.png"
                head_suffix = re.compile("jpg|png", re.I).findall(head_shot_source)[0] if re.compile("jpg|png", re.I).findall(head_shot_source) else "jpeg"
                head_shot = head_shot + str(int(time.time())) + "." + head_suffix
                filename = head_shot_path + head_shot
                urllib.request.urlretrieve(head_shot_source, filename=filename)
                print("head_shot:" + head_shot)
                # 获取讲师年龄
                age = random.randint(25, 50)
                print("age:" + str(age))
                
                # 写入数据库
                conn = pymysql.connect(host=host, port=port, user=user, password=password, db=database, charset=charset, cursorclass=pymysql.cursors.DictCursor)
                try:
                    with conn.cursor() as cursor:
                        cursor.execute('SELECT name FROM organizations_teacher WHERE name="{name}";'.format(name=name))
                        if cursor.fetchall(): # 记录已经存在
                            print("记录已经存在")
                            pass
                        else:
                            query_course_org_id_sql = "SELECT id FROM organizations_courseorg WHERE org_name='{org_name}'".format(org_name=org_name)
                            print("正在执行sql:" + query_course_org_id_sql)
                            cursor.execute(query_course_org_id_sql)
                            course_org_id = cursor.fetchall()[0]["id"]
                            print("course_org_id:" + str(course_org_id))
                            
                            insert_organizations_teacher_sql = """
                            INSERT INTO organizations_teacher(name, working_years, working_company, working_position, points, click_nums, fav_nums, add_time, course_org_id, head_shot, age) VALUES('{name}', {working_years}, '{working_company}', '{working_position}', '{points}', {click_nums}, {fav_nums}, '{add_time}', {course_org_id}, '{head_shot}', {age})
                            """.format(
                                name=name,
                                working_years=working_years,
                                working_company=working_company,
                                working_position=working_position,
                                points=points,
                                click_nums=click_nums,
                                fav_nums=fav_nums,
                                add_time=add_time,
                                course_org_id=course_org_id,
                                head_shot=head_shot,
                                age=age
                            )
                            print("正在执行sql:" + insert_organizations_teacher_sql)
                            cursor.execute(insert_organizations_teacher_sql)
                            conn.commit()
                except Exception as e:
                    traceback.print_exc()
                    logging.debug(e)
                    conn.rollback()
                finally:
                    conn.close()
                sub_browser.quit()

            q = queue.Queue(0)
            
            # 将teacher_urls放入同步队列中
            for teacher_url in teacher_urls:
                q.put(teacher_url)

            # 使用None作为队列结束标志
            q.put(None)

            # 生成1个线程
            Worker(i, q, func).start()

            # 当点击到最后一页时，自动退出
            if treedata.xpath("//div[@class='f-bg m-infomation']//a[@class='zbtn znxt js-disabled']") or not treedata.xpath("//div[@class='f-bg m-infomation']//a[contains(text(), '下一页')]"):
                break
            # 点击下一页按钮进入下一页
            browser.find_element_by_xpath("//div[@class='f-bg m-infomation']//a[@class='zbtn znxt']").click()
            time.sleep(2)

        except Exception as e:
            traceback.print_exc()
            logging.debug(traceback.format_exc())
        finally:
            i += 1
    
    # 关闭浏览器
    browser.quit()


if __name__ == "__main__":
    crawl_course_teacher(org_url="https://www.icourse163.org/university/TONGJI#/c", org_name="同济大学")


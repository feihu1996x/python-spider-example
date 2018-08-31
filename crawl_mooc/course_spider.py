#!/usr/bin/env python3

"""
@file: course_spider.py
@brief: 爬取机构课程
@author: feihu1996.cn
@date: 18-08-29
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
import redis

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

pool = redis.ConnectionPool(host=config.redis_host, port=config.redis_port)
db_redis = redis.Redis(connection_pool=pool, encoding='utf-8')

def crawl_course(org_url=None, org_name=None):
    """
    爬取机构课程
    """

    print("当前机构:%s" % org_name)

    # 课程难度
    level_list = ["初级", "中级", "高级"]
    
    # 打开浏览器
    browser = webdriver.Chrome()

    # 访问机构首页
    browser.get(org_url)
    time.sleep(5)

    # 自动翻页
    i = 0
    while True:
        try:
            data = browser.page_source
            treedata = etree.HTML(data)
            last_page_xpath = "//div[@id='j-courses']//a[@class='zbtn znxt']"
            no_next_page_xpath = "//div[@id='j-courses']//a[contains(text(), '下一页')]"
            no_next_page_xpath1 = "//div[@id='j-courses']//a[@class='zbtn znxt js-disabled']"
            course_url_xpath = "//div[@id='newCourseList']/div[@class='spocCourseList']/div[@class='list']//a/@href"

            print("当前正在爬取第%d页, %d" % (i+1, len(data)))            
            course_urls = [urljoin(org_url, item) for item in treedata.xpath(course_url_xpath)]

            print("当前课程列表长度:%d" % len(course_urls))

            def func(course_url, **kwargs):
                """
                课程详情处理函数
                """
                try:
                    # 打开浏览器
                    sub_browser = webdriver.Chrome()
                    sub_browser.get(course_url)                 
                    time.sleep(5)
                    course_data = sub_browser.page_source
                    tree_course_data = etree.HTML(course_data)

                    # open("test", "wb").write(course_data.encode("utf8"))

                    print("正在处理课程详情 %s, %d" % (course_url, len(course_data)))
                    
                    # 课程名称
                    name_xpath = "//div[@class='title-wrapper']/div[@class='f-cb f-pr']/div[@class='f-fl course-title-wrapper']/span[@class='course-title f-ib f-vam']/text()"
                    name = tree_course_data.xpath(name_xpath)
                    logging.debug(name[0])
                    name = ''.join([item for item in name if re.sub(r'[\?\s\xa0\u3000\u2002\ufeff]+', '', item)])
                    print("name:" + name)

                    # 课程描述
                    course_desc_xpath = '//div[@id="j-course-heading-intro"]/descendant-or-self::*/text()'
                    course_desc = tree_course_data.xpath(course_desc_xpath)
                    desc = ''.join([item for item in course_desc if re.sub(r'[\?\s\xa0\u3000\u2002\ufeff]+', '', item)])
                    print("desc:" + desc)

                    # 课程详情
                    detail_xpath = '//div[@id="content-section"]/div[@class="category-content j-cover-overflow"]'
                    detail = tree_course_data.xpath(detail_xpath)
                    detail = etree.tostring(detail[0], encoding='utf8').decode("utf8") if detail else ''
                    print("deatil:" + detail)

                    # 课程难度
                    level = random.choice(level_list)
                    print("level:" + level)

                    # 课程时长（分钟）
                    learning_time = random.randint(30, 1200)
                    print("learning_time:" + str(learning_time))
                    
                    # 学习人数
                    students_xpath = '//div[@id="course-enroll-info"]//span[@class="course-enroll-info_course-enroll_price-enroll_enroll-count"]/descendant-or-self::text()'
                    students_pattern = re.compile("\d{1,}")
                    students = tree_course_data.xpath(students_xpath)
                    students = ''.join([item for item in students if re.sub(r'[\?\s\xa0\u3000\u2002\ufeff]+', '', item)])
                    students = students_pattern.findall(students)
                    students = int(students[0]) if students else 0
                    print("students:" + str(students)) 

                    # 收藏数
                    fav_nums = random.randint(10, 10000)
                    print("fav_nums：" + str(fav_nums))

                    # 课程封面
                    cover_image_xpath = "//div[@id='j-courseImg']/img/@src"
                    cover_image = "resource/images/course_cover/2018/08/"
                    cover_image_path = "/mnt/usb/public/source/project/qinXueOnLine/media/"
                    cover_image_source = tree_course_data.xpath(cover_image_xpath)
                    cover_image_source = cover_image_source[0] if cover_image_source else ''
                    if not cover_image_source.startswith(('http', 'https')):
                        cover_image_source = "http://www.feihu1996.cn/img/logo.png"
                    cover_suffix = re.compile("jpg|png", re.I).findall(cover_image_source)[0] if re.compile("jpg|png", re.I).findall(cover_image_source) else "jpeg"
                    cover_image = cover_image + str(int(time.time())) + cover_suffix
                    filename = cover_image_path + cover_image
                    urllib.request.urlretrieve(cover_image_source, filename=filename)
                    print("cover_image:" + cover_image)
    
                    # 点击数
                    click_nums = random.randint(100, 10000)
                    print("click_nums:" + str(click_nums))

                    # 添加时间
                    add_time = datetime.datetime.now().strftime("%Y-%m-%d")
                    print("add_time:" + add_time)

                    # 课程机构
                    course_org_id = 0

                    # 课程类别
                    course_category_xpath = '//div[@id="j-breadcrumb"]/div[@class="breadcrumb"]/span[@class="breadcrumb_item"]/a/text()'
                    course_category = ','.join(tree_course_data.xpath(course_category_xpath))
                    course_category = re.sub(r'[\?\s\xa0\u3000\u2002\ufeff]+', '', course_category)
                    print("course_category:" + course_category)
                    
                    # 课程标签
                    course_tag = course_category
                    print("course_tag:" + course_tag)

                    # 课程讲师
                    teacher_xpath = "//div[@class='m-teachers']/div[@class='m-teachers_teacher-list']/a[1]/div[@class='cnt f-fl']/h3/text()"
                    teacher_name = tree_course_data.xpath(teacher_xpath)
                    teacher_name = ''.join([item for item in teacher_name if re.sub(r'[\?\s\xa0\u3000\u2002\ufeff]+', '', item)])
                    print("teacher_name:" + teacher_name)
                    teacher_id = 0

                    # 课程目标
                    course_target_pattern = re.compile('<span class="f-ib f-vam">授课目标</span>.*?</div>.*?<div class="category-content j-cover-overflow">.*?<div class="f-richEditorText">(.*?)</div>', re.S)
                    course_target = ''.join(course_target_pattern.findall(course_data))
                    course_target = re.sub(r'[\?\s\xa0\u3000\u2002\ufeff]+', '', course_target)
                    course_target = re.sub(r'<(/)?.*?>', '', course_target)
                    print("course_target:" + course_target)

                    # 课程须知
                    essential_skill_pattern = re.compile('<span class="f-ib f-vam">预备知识</span>.*?</div>.*?<div class="category-content j-cover-overflow">.*?<div class="f-richEditorText">(.*?)</div>', re.S)
                    essential_skill = ''.join(essential_skill_pattern.findall(course_data))
                    essential_skill = re.sub(r'[\?\s\xa0\u3000\u2002\ufeff]+|<(/)?.*?>', '', essential_skill)
                    print("essential_skill:" + essential_skill)
                    
                    # 写入数据库
                    try:
                        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=database, charset=charset, cursorclass=pymysql.cursors.DictCursor)
                        with conn.cursor() as cursor:
                            # 获取teacher_id
                            cursor.execute("SELECT id FROM organizations_teacher WHERE name='{teacher_name}'".format(teacher_name=teacher_name))
                            data_list = cursor.fetchall()
                            if data_list:
                                teacher_id = data_list[0]["id"]
                            else:
                                teacher_id = 0
                            print("teacher_id:" + str(teacher_id))
                            
                            # 获取course_org_id
                            cursor.execute("SELECT id FROM organizations_courseorg WHERE org_name='{org_name}'".format(org_name=org_name))
                            data_list = cursor.fetchall()
                            if data_list:
                                course_org_id = data_list[0]["id"]
                            else:
                                course_org_id = 0
                            print("course_org_id:" + str(course_org_id))

                            # 插入数据
                            insert_courses_course_sql = """
                            INSERT INTO courses_course
                                    (name, 
                                    `desc`, 
                                    detail, 
                                    level, 
                                    learning_time, 
                                    students, 
                                    fav_nums, 
                                    cover_image, 
                                    click_nums, 
                                    add_time, 
                                    course_org_id, 
                                    course_category, 
                                    course_tag, 
                                    teacher_id, 
                                    course_target, 
                                    essential_skill, 
                                    is_banner) 
                            VALUES  ('{name}', 
                                    '{desc}', 
                                    '{detail}', 
                                    '{level}', 
                                    {learning_time}, 
                                    {students}, 
                                    {fav_nums}, 
                                    '{cover_image}', 
                                    {click_nums}, 
                                    '{add_time}', 
                                    {course_org_id}, 
                                    '{course_category}', 
                                    '{course_tag}', 
                                    {teacher_id}, 
                                    '{course_target}', 
                                    '{essential_skill}', 
                                    {is_banner})    
                            """.format(
                                name=name, 
                                desc=desc, 
                                detail=detail, 
                                level=level, 
                                learning_time=learning_time, 
                                students=students, 
                                fav_nums=fav_nums, 
                                cover_image=cover_image, 
                                click_nums=click_nums, 
                                add_time=add_time, 
                                course_org_id=course_org_id, 
                                course_category=course_category, 
                                course_tag=course_tag, 
                                teacher_id=teacher_id, 
                                course_target=course_target, 
                                essential_skill=essential_skill, 
                                is_banner=0)
                            print("正在插入数据:%s" % insert_courses_course_sql)
                            cursor.execute(insert_courses_course_sql)
                            conn.commit()
                            # 将成功处理的course_url放入redis
                            db_redis.lpush("course_list", course_url)        
                        
                    except:
                        print("exception in mysql conn")
                        conn.rollback()
                        logging.debug(traceback.format_exc())
                        traceback.print_exc()
                        db_redis.lpush("failed_course_item", course_url)
                    finally:
                        conn.close()
            
                except:
                    print("exception in func")
                    traceback.print_exc()
                    logging.debug(traceback.format_exc())
                    db_redis.lpush("failed_course_item", course_url)
                finally:
                    sub_browser.quit() 
                    
             
            # 多线程处理当前课程列表页
            # 如果有多页，则一页一个线程，
            # 如果只有一页，则一个course_url一个线程
            if course_urls:
                q = queue.Queue(0)
                for course_url in course_urls:
                    q.put(course_url)
                if not treedata.xpath(no_next_page_xpath): # 课程信息只有一页
                    worker_nums = len(course_urls)
                    for j in range(0, worker_nums):
                        q.put(None)
                    for j in range(0, worker_nums):
                        Worker(j, q, func).start()
                    print("创建了%d个线程" % worker_nums)
                else:   # 课程信息有多页
                    worker_nums = 1
                    q.put(None)
                    Worker(i, q, func).start()
                    print("创建了%d个线程" % worker_nums)
 
            # 当点击到最后一页时，自动退出
            if treedata.xpath(no_next_page_xpath1) or not treedata.xpath(no_next_page_xpath):
                break

            # 点击下一页按钮进入下一页
            browser.find_element_by_xpath(last_page_xpath).click()
            time.sleep(5)
        except:
            print("exception in while loop")
            traceback.print_exc()
            logging.debug(traceback.format_exc()) 
            # 在爬取当前页时出现异常，调转到下一页,
            # 若没有下一页，则跳出循环
            if treedata.xpath(no_next_page_xpath):
                browser.find_element_by_xpath(last_page_xpath).click()
                time.sleep(5)
            else:
                break
        finally:
            i += 1
     
    # 关闭浏览器
    browser.quit()
        
if __name__ == "__main__":
    length = db_redis.llen("org_list")
    item = eval(db_redis.lindex("org_list", random.randint(0, length-1)).decode("utf8"))
    crawl_course(org_url=item["org_url"], org_name=item["org_name"])
    db_redis.delete("course_list")

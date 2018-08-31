#!/usr/bin/env python3

"""
@file: course_comment_spider.py 
@brief: 课程评论爬虫
@author: feihu1996.cn
@date: 18-08-30
@version: 1.0
"""

import urllib.request
import random
import re
import time
import threading
import logging
import traceback
import queue
import datetime

from lxml import etree
import redis
from selenium import webdriver
import pymysql

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


address_list = [
    "回龙观街道文华西路育荣教育园区",
    "德国勃兰登堡州波茨坦",
    "杭州市学院路35号浙江教育综合大楼",
    "金华市义乌市学院路2号",
    "北京市西城区德外大街4号C座10层",
    "北京市海淀区北四环中路238号柏彦大厦5层506室",
    "湖北省武汉市南湖大道水蓝路津发小区16幢201号",
    "北京市西城区德外大街4号C座10层",
    "河南省焦作市山阳区世纪大道2001号"
]

class Worker(threading.Thread):
    def __init__(self, index, queue):
        threading.Thread.__init__(self)
        self.index = index
        self.queue = queue
    def run(self):
        try:
            browser = webdriver.Chrome()
            while 1:
                try:
                    # 从同步队列中获取对象
                    item = self.queue.get()

                    # 循环终止条件
                    if item is None:
                        break

                    # 访问课程页面
                    print("正在处理%s"%item)
                    browser.get(item)
                    time.sleep(1)

                    # 跳转到评论页面
                    print("正在跳转到评论页面...")
                    browser.find_element_by_xpath("//div[@id='review-tag-button']").click()
                    time.sleep(1.5)

                    # 自动翻页，获取所有评论
                    i = 0
                    while True:
                        try:
                            data = browser.page_source
                            treedata = etree.HTML(data)

                            print("正在处理第%d页的评论"%(i+1))
                            
                            course_name_xpath = "//div[@class='title-wrapper']/div[@class='f-cb f-pr']/div[@class='f-fl course-title-wrapper']/span[@class='course-title f-ib f-vam']/text()"
                            course_name = treedata.xpath(course_name_xpath)
                            logging.debug(course_name[0])
                            course_name = ''.join([item for item in course_name if re.sub(r'[\?\s\xa0\u3000\u2002\ufeff]+', '', item)])

                            comment_list = []
                            comment_list = treedata.xpath("//div[@class='ux-mooc-comment-course-comment_comment-list_item']")
                            print("当前评论队列长度为:%d" %(len(comment_list)))
                            for comment in comment_list:
                                try:
                                    print("正在处理评论:", comment)
                                    print("test user_name_xpath:", comment.xpath("div[@class='ux-mooc-comment-course-comment_comment-list_item_body']/div[@class='ux-mooc-comment-course-comment_comment-list_item_body_user-info']/a/text()"))
                                    print("test head_shot_xpath:", comment.xpath("div[@class='ux-mooc-comment-course-comment_comment-list_item_avatar']/a/img/@src"))
                                    print("test comment_content_xpath:", comment.xpath("div[@class='ux-mooc-comment-course-comment_comment-list_item_body']/div[@class='ux-mooc-comment-course-comment_comment-list_item_body_content']/span/text()"))

                                    # 用户密码
                                    password = "qinXueOnLine"
                                    
                                    # 用户权限
                                    is_superuser = 0
                                    is_staff = 0
                                    is_active = 1
            
                                    # 用户昵称
                                    nick_name = str(int(time.time()))
                                    first_name = ""
                                    last_name = ""
                                    
                                    # 用户邮箱
                                    email = "%s@qinxueonline.com" %(nick_name)

                                    # 用户注册日期
                                    date_joined = datetime.datetime.now().strftime("%Y-%m-%d")

                                    # 用户名
                                    user_name_xpath= "div[@class='ux-mooc-comment-course-comment_comment-list_item_body']/div[@class='ux-mooc-comment-course-comment_comment-list_item_body_user-info']/a/text()"
                                    user_name = ''.join(comment.xpath(user_name_xpath))
                                    user_name = re.sub(r'[\?\s\xa0\u3000\u2002\ufeff]+', '', user_name)

                                    # 用户生日
                                    birthday = date_joined
                                    date_joined = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

                                    # 用户性别
                                    gender = random.choice(["male", "female"])

                                    # 用户地址
                                    address = random.choice(address_list) 
                                   
                                    # 用户手机
                                    cell_phone_number = ''.join([str(random.randint(0,9)) for i in range(0, 11)])


                                    # 评论课程
                                    course_id = 0

                                    # 添加时间
                                    add_time = datetime.datetime.now().strftime("%Y-%m-%d")
                                        
                                    # 评论内容
                                    comment_content_xpath = "div[@class='ux-mooc-comment-course-comment_comment-list_item_body']/div[@class='ux-mooc-comment-course-comment_comment-list_item_body_content']/span/text()"
                                    comment_content = ''.join(comment.xpath(comment_content_xpath))
                                    comment_content = re.sub(r'[\?\s\xa0\u3000\u2002\ufeff]+', '', comment_content)
                                    print("comment_content:", comment_content)

                                    # 链接数据库
                                    conn = pymysql.connect(host=host, port=port, user=user, password=db_password, db=database, charset=charset, cursorclass=pymysql.cursors.DictCursor)
                                    try:
                                        with conn.cursor() as cursor:
                                            query_user_sql = "SELECT id FROM users_userprofile WHERE username='{user_name}'".format(user_name=user_name) 
                                            print('正在执行sql,', query_user_sql)
                                            cursor.execute(query_user_sql)

                                            if not cursor.fetchall(): # 查找注册用户
                                                # 用户头像
                                                head_shot_xpath = "div[@class='ux-mooc-comment-course-comment_comment-list_item_avatar']/a/img/@src"
                                                head_shot = "resource/images/head_shot/2018/08/"
                                                head_shot_path = "/mnt/usb/public/source/project/qinXueOnLine/media/"
                                                head_shot_source = ''.join(comment.xpath(head_shot_xpath))
                                                if not head_shot_source.startswith(('http', 'https')):
                                                    head_shot_source = "http://www.feihu1996.cn/img/logo.png"
                                                head_suffix = re.compile("jpg|png", re.I).findall(head_shot_source)[0] if re.compile("jpg|png", re.I).findall(head_shot_source) else "jpeg"
                                                head_shot = head_shot + str(int(time.time())) + "." + head_suffix
                                                filename = head_shot_path + head_shot
                                                try:
                                                    urllib.request.urlretrieve(head_shot_source, filename=filename)
                                                except:
                                                    head_shot_source = "http://www.feihu1996.cn/img/logo.png"
                                                    urllib.request.urlretrieve(head_shot_source, filename=filename) 
                                                print("正在注册用户...")
                                                # 创建用户
                                                sql = """
                                                INSERT INTO users_userprofile
                                                        (
                                                        password,
                                                        is_superuser,
                                                        username,
                                                        first_name,
                                                        last_name,
                                                        email,
                                                        is_staff,
                                                        is_active,
                                                        date_joined,
                                                        nick_name,
                                                        birthday,
                                                        gender,
                                                        address,
                                                        cell_phone_number,
                                                        head_shot
                                                        )
                                                VALUES  (
                                                        '{password}',
                                                        {is_superuser},
                                                        '{username}',
                                                        '{first_name}',
                                                        '{last_name}',
                                                        '{email}',
                                                        {is_staff},
                                                        {is_active},
                                                        '{date_joined}',
                                                        '{nick_name}',
                                                        '{birthday}',
                                                        '{gender}',
                                                        '{address}',
                                                        '{cell_phone_number}',
                                                        '{head_shot}'
                                                        )
                                                """.format(
                                                    password =  password,
                                                    is_superuser = is_superuser,
                                                    username = user_name,
                                                    first_name = first_name,
                                                    last_name = last_name,
                                                    email = email,
                                                    is_staff = is_staff,
                                                    is_active = is_active,
                                                    date_joined = date_joined,
                                                    nick_name = nick_name,
                                                    birthday = birthday,
                                                    gender = gender,
                                                    address = address,
                                                    cell_phone_number = cell_phone_number,
                                                    head_shot = head_shot
                                                )
                                                print('正在执行sql,', sql)
                                                cursor.execute(sql)
                                                conn.commit()

                                            # 获取user_id
                                            print("正在获取user_id")
                                            cursor.execute(query_user_sql)
                                            data_list = cursor.fetchall()
                                            user_id = data_list[0]["id"] if data_list else 0
                                            print("user_id:", user_id)
                                             
                                            # 获取course_id
                                            print("正在获取course_id")
                                            cursor.execute("SELECT id FROM courses_course WHERE name='{course_name}'".format(course_name=course_name))
                                            data_list = cursor.fetchall()
                                            if data_list:
                                                course_id = data_list[0]["id"]
                                            else:
                                                course_id = 0
                                            print("course_id:", course_id)
    
                                            # 写入评论数据
                                            print("正在写入评论数据...")
                                            sql = """
                                            INSERT INTO userOperations_coursecomments
                                                    (
                                                    comment_content,
                                                    add_time,
                                                    course_id,
                                                    user_id
                                                    )
                                            VALUES  (
                                                    '{comment_content}',
                                                    '{add_time}',
                                                    {course_id},
                                                    {user_id}
                                                    )        
                                            """.format(
                                                comment_content = comment_content,
                                                add_time = add_time,
                                                course_id = course_id,
                                                user_id = user_id
                                            )
                                            print("正在执行sql ...")
                                            cursor.execute(sql)
                                            conn.commit()
                                    except:
                                        traceback.print_exc()
                                        logging.debug(traceback.format_exc())
                                        conn.rollback()
                                except:
                                    traceback.print_exc()
                                    logging.debug(traceback.format_exc())

                            # 如果是最后一页,则退出循环
                            if treedata.xpath("//div[@class='ux-mooc-comment-course-comment_pager']/ul/li[@class='ux-pager_btn ux-pager_btn__next']/a[@class='th-bk-disable-gh']") or not treedata.xpath("//div[@class='ux-mooc-comment-course-comment_pager']/ul/li[@class='ux-pager_btn ux-pager_btn__next']/a[contains(text(), '下一页')]"):
                                print("当前已经是最后一页")
                                break

                            # 跳转到下一页
                            browser.find_element_by_xpath("//div[@class='ux-mooc-comment-course-comment_pager']/ul/li[@class='ux-pager_btn ux-pager_btn__next']/a[@class='th-bk-main-gh']").click()
                            time.sleep(1.5)
                        except:
                            traceback.print_exc()
                            logging.debug(traceback.format_exc())
                            browser.find_element_by_xpath("//div[@class='ux-mooc-comment-course-comment_pager']/ul/li[@class='ux-pager_btn ux-pager_btn__next']/a[@class='th-bk-main-gh']").click()
                            time.sleep(1.5)
                        finally:
                            i += 1
    
                    print("index:",self.index, "task", item, "finished")
                    self.queue.task_done()
                except:
                    traceback.print_exc()
                    logging.debug(traceback.format_exc())
        except:
            traceback.print_exc()
            logging.debug(traceback.format_exc())
        finally:
            browser.quit()

course_urls = [item.decode("utf8") for item in db_redis.lrange("course_list", 0, -1)]

# 生成一个不限制长度的同步队列
q = queue.Queue(0)

# 将所有要处理的course_url放入同步队列中
for course_url in course_urls:
    q.put(course_url)

for i in range(0, 10):
    q.put(None)

# 生成10个线程
for i in range(0, 10):
    Worker(i, q).start()


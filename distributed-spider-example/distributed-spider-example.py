"""
这只爬虫应当部署在分布式架构中的各个子节点中
"""

import redis
import pymysql
import urllib.request
import re


rconn=redis.Redis("172.17.0.8","6379")
#url:http://www.17k.com/book/2.html
'''
url-i-"1"
'''
for i in range(0,5459058):
    # 判断当前资源是否已经被其他机器上的爬虫爬取了
    isdo=rconn.hget("url",str(i))
    if(isdo!=None):
        continue

    # 将当前已爬取的资源写入redis并打上标记   
    rconn.hset("url",str(i),"1")

    try:
        data=urllib.request.urlopen("http://www.17k.com/book/"+str(i)+".html").read().decode("utf-8","ignore")
    except Exception as err:
        print(str(i)+str(err))
        continue
    pat='<a class="red" .*?>(.*?)</a>'
    rst=re.compile(pat,re.S).findall(data)
    if(len(rst)==0):
        continue
    name=rst[0]

    # 将爬取目标（小说名）写入数据中心
    rconn.hset("rst",str(i),str(name))

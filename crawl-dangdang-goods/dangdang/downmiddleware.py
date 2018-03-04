from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
from dangdang.settings import IPPOOL
import urllib.request
import random

class IPPOOLS(HttpProxyMiddleware):
    def __init__(self,ip=""):
        self.ip=ip
    def process_request(self, request, spider):
        '''
        #先随机选择一个IP
        thisip=random.choice(IPPOOL)
        print(thisip["ipaddr"])
        #print("hello")
        thisip="127.0.0.1:8888"
        '''
        # 另外一种构建代理ip池的方式，通过API接口去调用
        thisip = urllib.request.urlopen("http://tvp.daxiangdaili.com/ip/?tid=557722557818358&num=1&foreign=on").read().decode("utf-8", "ignore")
        print(thisip)
        #真实地将当前得到的ip添加到咱们的请求中，即使用代理IP进行访问
        #request.meta["proxy"]=thisip["ipaddr"]
        request.meta["proxy"] = thisip

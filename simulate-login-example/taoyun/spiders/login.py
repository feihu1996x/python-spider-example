# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest

class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["iqianyue.com"]
    #start_urls = ['http://iqianyue.com/']
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}
    # 编写start_requests()方法，第一次会默认调取该方法中的请求
    def start_requests(self):
        # 首先爬一次登录页，然后进入回调函数parse()
        return [Request("http://edu.iqianyue.com/index_user_login.html", meta={"cookiejar": 1}, callback=self.parse)]

    def parse(self, response):
        # 设置要传递的post信息，此时没有验证码字段
        data = {
            "number": "weijc",
            "passwd": "weijc7789",
            }

        print("登录中…")
        # 通过FormRequest.from_response()进行登陆
        return [FormRequest.from_response(response,
                                        # 设置cookie信息
                                        meta={"cookiejar": response.meta["cookiejar"]},
                                        # 设置headers信息模拟成浏览器
                                        headers=self.header,
                                        # 设置post表单中的数据
                                        formdata=data,
                                        # 设置回调函数，此时回调函数为next()
                                        callback=self.next,
                                       )]
                                       
    def next(self,response):
        data=response.body
        fh=open("a.html","wb")
        fh.write(data)
        fh.close()
        print(response.xpath("/html/head/title/text()").extract())
        yield Request("http://edu.iqianyue.com/index_user_index",callback=self.next2,meta={"cookiejar": True})
    
    def next2(self,response):
        data=response.body
        fh = open("b.html", "wb")
        fh.write(data)
        fh.close()
        print(response.xpath("/html/head/title/text()").extract())
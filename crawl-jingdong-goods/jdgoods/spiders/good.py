# -*- coding: utf-8 -*-
import random
import re
import urllib.request

import scrapy
from jdgoods.items import JdgoodsItem
from scrapy.http import Request


class GoodSpider(scrapy.Spider):
    name = "good"
    allowed_domains = ["jd.com"]
    #start_urls = ['http://jd.com/']
    def start_requests(self):
        ua=["User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"]
        req1=urllib.request.Request("https://book.jd.com/")
        req1.add_header("User-Agent",random.choice(ua))
        allpddata=urllib.request.urlopen(req1).read().decode("utf-8","ignore")
        pat1='<h3><a href="..(channel.jd.com.*?.html)"'
        allpd=re.compile(pat1).findall(allpddata)
        catall=[]
        for i in allpd:
            thispd="http://"+i
            req2 = urllib.request.Request(thispd)
            req2.add_header("User-Agent", random.choice(ua))
            pddata=urllib.request.urlopen(req2).read().decode("utf-8", "ignore")
            #print(len(pddata))
            pat2='href="..list.jd.com.list.html.cat=([0-9,]*?)[&"]'
            catdata=re.compile(pat2).findall(pddata)
            for j in catdata:
                catall.append(j)
        #print(len(catall))
        print(catall[0])
        catall2=set(catall)
        #print(len(catall2))
        #获得页数
        allurl=[]#[{"cat":"pagenum"}]
        x=0
        for m in catall2:
            thispdnum=m
            req3 = urllib.request.Request("https://list.jd.com/list.html?cat="+thispdnum)
            req3.add_header("User-Agent", random.choice(ua))
            listdata = urllib.request.urlopen(req3).read().decode("utf-8", "ignore")
            pat3="<em>共<b>(.*?)</b>页"
            allpage=re.compile(pat3).findall(listdata)
            if(len(allpage)>0):
                pass
            else:
                allpage=[1]
            allurl.append({thispdnum:allpage[0]})
            #为了测试
            if(x>2):
                break
            x+=1
        x=0
        for n in catall2:
            thispage=allurl[x][n]
            for p in range(1,int(thispage)+1):
                thispageurl="https://list.jd.com/list.html?cat="+str(n)+"&page="+str(p)
                print(thispageurl)
                yield Request(thispageurl,callback=self.parse)
            x+=1
            
    def parse(self, response):
        item=JdgoodsItem()
        listdata=response.body.decode("utf-8","ignore")
        #频道1、2
        pd=response.xpath("//span[@class='curr']/text()").extract()
        if(len(pd)==0):
            pd=["缺省","缺省"]
        if(len(pd)==1):
            pda=pd[0]
            pd=[pda,"缺省"]
        pd1=pd[0]
        pd2=pd[1]
        print(pd1)
        #图书名(从下标为3的地方开始取)
        bookname=response.xpath("//div[@class='p-name']/a/em/text()").extract()
        print(bookname[0])
        #价格https://p.3.cn/prices/mgets?callback=jQuery5975516&type=1&skuIds=J_10924526
        allskupat='<a data-sku="(.*?)"'
        allsku=re.compile(allskupat).findall(listdata)
        print(allsku)
        #评论数https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds=10650505&callback=jQuery599131
        #作者
        author=response.xpath("//span[@class='author_type_1']/a/@title").extract()
        #出版社
        pub=response.xpath("//span[@class='p-bi-store']/a/@title").extract()
        #店家
        seller=response.xpath("//span[@class='curr-shop']/text()").extract()
        #处理当前页的数据
        for n in range(0,len(seller)):
            name=bookname[n+3]
            thissku=allsku[n]
            priceurl="https://p.3.cn/prices/mgets?callback=jQuery5975516&type=1&skuIds=J_"+str(thissku)
            pricedata=urllib.request.urlopen(priceurl).read().decode("utf-8","ignore")
            pricepat='"p":"(.*?)"'
            price=re.compile(pricepat).findall(pricedata)[0]
            pnumurl = "https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds="+str(thissku)+"&callback=jQuery599131"
            pnumdata = urllib.request.urlopen(pnumurl).read().decode("utf-8", "ignore")
            pnumpat = '"CommentCount":(.*?),'
            pnum = re.compile(pnumpat).findall(pnumdata)[0]
            thisauthor=author[n]
            #print(author)
            thispub=pub[n]
            thisseller=seller[n]
            #print(pub)
            #print(seller)
            #print(author)
            print(pd1)
            print(pd2)
            print(name)
            print(price)
            print(pnum)
            print(thisauthor)
            print(thispub)
            print(thisseller)
            item["pd1"]=pd1
            item["pd2"]=pd2
            item["name"]=name
            item["price"]=price
            item["pnum"]=pnum
            item["author"]=thisauthor
            item["pub"]=thispub
            item["seller"]=thisseller
            yield item

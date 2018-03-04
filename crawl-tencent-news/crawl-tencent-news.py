'''
1、爬取新闻首页
2、得到各新闻链接
3、爬取新闻链接
4、寻找有没有frame
5、若有，抓取frame下对应网页内容
6、若没有，直接抓取当前页面
'''
import urllib.request
import re


url="http://news.qq.com/"
data=urllib.request.urlopen(url).read().decode("UTF-8","ignore")
pat1='<a target="_blank" class="linkto" href="(.*?)"'
alllink=re.compile(pat1).findall(data)
for i in range(0,len(alllink)):
    thislink=alllink[i]
    thispage=urllib.request.urlopen(thislink).read().decode("gb2312","ignore")
    pat2="<frame src=(.*?)>"
    isframe=re.compile(pat2).findall(thispage)
    if(len(isframe)==0):
        #直接爬
        print(i)
        urllib.request.urlretrieve(thislink,str(i)+".html")
    else:
        #得到frame的网址爬
        flink=isframe[0]
        urllib.request.urlretrieve(flink,str(i)+".html")
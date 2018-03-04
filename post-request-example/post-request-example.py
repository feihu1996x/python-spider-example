import urllib.request
import urllib.parse

posturl="http://www.iqianyue.com/mypost/"
postdata=urllib.parse.urlencode({
    "name":"ceo@txk7.com",
    "pass":"kjsahgjkashg",
    }).encode("utf-8")
# 进行post请求，就需要使用urllib.request下面的Request(真实post地址,post数据)
req=urllib.request.Request(posturl,postdata)
rst=urllib.request.urlopen(req).read().decode("utf-8")
fh=open("post.html","w")
fh.write(rst)
fh.close()
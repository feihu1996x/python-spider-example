#IP代理池构建的第一种方案(适合于代理IP稳定的情况)
import random
import urllib.request


ippools=[
    "68.13.196.233:8080",
    "112.247.100.200:9999",
    "112.247.5.22:9999",
    ]

def ip(ippools):
    thisip=random.choice(ippools)
    print(thisip)
    proxy=urllib.request.ProxyHandler({"http":thisip})
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)

for i in range(0,5):
    try:
        ip(ippools)
        url="http://www.baidu.com"
        data1=urllib.request.urlopen(url).read()
        data=data1.decode("utf-8","ignore")
        print(len(data))
        fh=open("ip_baidu_"+str(i)+".html","wb")
        fh.write(data1)
        fh.close()
    except Exception as err:
        print(err)
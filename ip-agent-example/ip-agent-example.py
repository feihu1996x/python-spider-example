import urllib.request

ip="68.13.196.233:8080"
proxy=urllib.request.ProxyHandler({"http":ip})
opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
urllib.request.install_opener(opener)
url="http://www.baidu.com"
data1=urllib.request.urlopen(url).read()
data=data1.decode("utf-8","ignore")
print(len(data))
fh=open("ip_baidu.html","wb")
fh.write(data1)
fh.close()
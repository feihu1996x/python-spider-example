import urllib.request


url="http://blog.csdn.net"
#头文件格式header=("User-Agent",具体用户代理值)
headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
opener=urllib.request.build_opener()
opener.addheaders=[headers]
data=opener.open(url).read()
fh=open("ua.html","wb")
fh.write(data)
fh.close()
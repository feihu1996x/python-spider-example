import urllib.request
import re

url="http://blog.csdn.net/"
headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
opener=urllib.request.build_opener()
opener.addheaders=[headers]
# 安装为全局
urllib.request.install_opener(opener)
data=urllib.request.urlopen(url).read().decode("utf-8","ignore")
pat='<h3  class="tracking-ad" data-mod="popu_254"><a href="(.*?)"'
alllink=re.compile(pat).findall(data)
#print(alllink)
for i in range(0,len(alllink)):
    localpath=str(i)+".html"
    thislink=alllink[i]
    urllib.request.urlretrieve(thislink,filename=localpath)
    print("当前文章(第"+str(i)+"篇）爬取成功！")
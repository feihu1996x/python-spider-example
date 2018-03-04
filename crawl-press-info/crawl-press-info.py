import urllib.request
import re

data=urllib.request.urlopen("https://read.douban.com/provider/all").read().decode("utf-8")
pat='<div class="name">(.*?)</div>'
rst=re.compile(pat).findall(data)
fh=open("pressInfo.txt","w")
for i in range(0,len(rst)):
    print(rst[i])
    fh.write(rst[i]+"\n")
fh.close()
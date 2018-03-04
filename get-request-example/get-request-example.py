import urllib.request,re

keywd="诗意代码"
keywd=urllib.request.quote(keywd)
#page=(num-1)*10
for i in range(1,11):
    url="http://www.baidu.com/s?wd="+keywd+"&pn="+str((i-1)*10)
    data=urllib.request.urlopen(url).read().decode("utf-8")
    pat="title:'(.*?)',"
    pat2='"title":"(.*?)",'
    rst1=re.compile(pat).findall(data)
    rst2=re.compile(pat2).findall(data)
    for j in range(0,len(rst1)):
        print(rst1[j])
    for z in range(0,len(rst2)):
        print(rst2[z])
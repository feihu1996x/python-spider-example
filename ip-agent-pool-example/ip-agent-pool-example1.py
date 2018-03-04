#IP代理池实现的第二种方式（接口调用法，这种方法更适合于代理IP不稳定的情况）
import urllib.request


def api():
    print("这一次调用了接口")
    thisall=urllib.request.urlopen("http://tvp.daxiangdaili.com/ip/?tid=559126871522487&num=10&foreign=only")
    ippools=[]
    for item in thisall:
        ippools.append(item.decode("utf-8","ignore"))
    return ippools

def ip(ippools,time):
    thisip=ippools[time]
    print("当前用的IP是："+ippools[time])
    proxy=urllib.request.ProxyHandler({"http":thisip})
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    
x=0
for i in range(0,35):
    try:
        if(x%10==0):
            time=x%10
            ippools=api()
            ip(ippools,time)
        else:
            time=x%10
            ip(ippools,time)
        url="http://www.baidu.com"
        data1=urllib.request.urlopen(url).read()
        data=data1.decode("utf-8","ignore")
        print(len(data))
        fh=open(str(i)+".html","wb")
        fh.write(data1)
        fh.close()
        x+=1
    except Exception as err:
        print(err)
        x+=1
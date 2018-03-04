'''
URLError出现的原因：
1）连不上服务器
2）远程url不存在
3）无网络
4）触发HTTPError
'''

import urllib.request
import urllib.error


try:
    urllib.request.urlopen("http://blog.csdn.net")
except urllib.error.URLError as e:
    if hasattr(e,"code"):
        print(e.code)
    if hasattr(e,"reason"):
        print(e.reason)
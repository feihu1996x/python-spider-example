#!/usr/bin/env python3

"""
@file: worker.py
@brief: 多线程处理类
@author: feihu1996.cn
@date: 18-08-29
@version: 1.0
"""

import threading
import logging
import traceback

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',               
                    filename='spider.log',
                    filemode='a')

class Worker(threading.Thread):
    def __init__(self, index, queue, func):
        threading.Thread.__init__(self)
        self.index = index
        self.queue = queue
        self.func = func
    def run(self):
        while 1:  
            # 从同步队列中获取对象
            item = self.queue.get()

            # 循环终止条件
            if item is None:
                break

            self.func(item)                
                
            print("index:",self.index, "task", item, "finished")
            self.queue.task_done()

if __name__ == "__main__":
    def func(item):
        print(item**item)
    import queue
    q = queue.Queue(0)
    for i in range(0, 10):
        q.put(i)
    for i in range(0, 10):
        Worker(i, q, func).start()

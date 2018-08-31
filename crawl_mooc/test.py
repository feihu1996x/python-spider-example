import queue

from worker import Worker


q = queue.Queue(0)

def func(item):
    print(item**item)

while True:
    a = 0
    a += 1
    
    for i in range(100):
        q.put(i)

    for i in range(10):
        q.put(None)

    for i in range(10):
        Worker(i, q, func).start()

    if a > 1000:
        break


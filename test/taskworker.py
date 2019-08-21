# task_worker.py
# coding=utf-8

# 多进程分布式例子
# 非服务端：worker

import random, time, sys, queue,multiprocessing
from multiprocessing.managers import BaseManager


# 创建类似的QueueManager
class QueueManager(BaseManager):
    pass


# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字即可
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行task_master.py的机器
server_addr = '192.168.0.16' # '127.0.0.1'
print('connect to server %s...' % server_addr)
# 端口和验证码注意要保持完全一致
m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
# 从网络连接
m.connect()
# 获取Queue的对象
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列获取任务，并把结果写入result队列
for i in range(100):
    try:
        n = task.get()
        task.put(random.randint(0, 10000))
        print('run task %d * %d...' % (n, n))
        r = '%d * %d = %d' % (n, n, n * n)
        time.sleep(1)
        result.put(r)
    except queue.Empty:
        print('task queue is empty')
# 处理结果
print('worker exit')
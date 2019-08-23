# task_worker.py
# coding=utf-8

# 多进程分布式例子
# 非服务端：worker


from multiprocessing.managers import BaseManager
from common.RuleConf import *
import json

# 创建类似的QueueManager
class QueueManager(BaseManager):
    pass




def worker():
    # 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字即可
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')

    # 连接到服务器，也就是运行task_master.py的机器
    server_addr = '192.168.0.16'  # '127.0.0.1'
    print('connect to server %s...' % server_addr)
    # 端口和验证码注意要保持完全一致
    m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
    # 从网络连接
    m.connect()
    # 获取Queue的对象
    task = m.get_task_queue()
    result = m.get_result_queue()

    # 从task队列获取任务，并把结果写入result队列
    n = task.get()
    while n:
        time.sleep(1)
        result.put({"data": n, "code": 1})

        crawler = PageCrawler()
        conf = json.loads(n['contentInfo'])
        print(conf)
        crawler.runProcess(conf=conf)
        n = task.get()

if __name__ == '__main__':
    worker()
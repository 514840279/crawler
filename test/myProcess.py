# -*- coding:utf-8 -*-

"""
Process常用属性与方法：
    name:进程名
    pid：进程id
    run()，自定义子类时覆写
    start()，开启进程
    join(timeout=None)，阻塞进程
    terminate(),终止进程
    is_alive()，判断进程是否存活
"""

import os, time
from multiprocessing import Process


def worker():
    print("子进程执行中>>> pid={0},ppid={1}".format(os.getpid(), os.getppid()))
    time.sleep(5)
    print("子进程终止>>> pid={0}".format(os.getpid()))


def main():
    print("主进程执行中>>> pid={0}".format(os.getpid()))

    ps = []
    # 创建子进程实例
    for i in range(20):
        p = Process(target=worker, name="worker" + str(i), args=())
        ps.append(p)

    # 开启进程
    for i in range(20):
        ps[i].start()

    # 阻塞进程
    for i in range(20):
        ps[i].join()

    print("主进程终止")


if __name__ == '__main__':
    main()

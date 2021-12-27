# -*- coding: utf-8 -*-

# @File    : multiprocess_test.py
# @Date    : 2021-12-23
# @Author  : windyzhao
# from multiprocessing import Pool
import random
import time
from multiprocessing import Process, Lock, Pool
import os
import multiprocessing as mp


# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())
#
#
# def f(name):
#     info('function f')
#     print('hello', name)
#
#
# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()

# def foo(q):
#     q.put('hello')
#
#
# if __name__ == '__main__':
#     mp.set_start_method('spawn')
#     q = mp.Queue()
#     p = mp.Process(target=foo, args=(q,))
#     p.start()
#     print(q.get())
#     p.join()

# def fun1(name):
#     print('测试%s多进程' % name)
#
#
# if __name__ == '__main__':
#     process_list = []
#     for i in range(5):  # 开启5个子进程执行fun1函数
#         p = Process(target=fun1, args=(f'Python_{i}',))  # 实例化进程对象
#         p.start()
#         process_list.append(p)
#
#     for j in process_list:
#         j.join()
#
#     print('结束测试')


def f(x):
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    return x * x


if __name__ == '__main__':
    args = range(10)
    with Pool(processes=1) as pool:  # start 4 worker processes
        res = pool.imap(f, args)
        pool.close()
        pool.join()
        print("res")
        print(res)
        while 1:
            try:
                print(next(res))
            except StopIteration:
                break

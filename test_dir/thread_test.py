# -*- coding: utf-8 -*-

# @File    : thread_test.py
# @Date    : 2021-12-24
# @Author  : windyzhao
from concurrent.futures._base import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep
import threading
import random

# def music(music_name):
#     for i in range(2):
#         print('正在听{}'.format(music_name))
#         sleep(1)
#         print('music over')
#
#
# def game(game_name):
#     for i in range(2):
#         print('正在玩{}'.format(game_name))
#         sleep(3)
#         print('game over')
#
#
# threads = []
# t1 = threading.Thread(target=music, args=('稻香',))
# threads.append(t1)
# t2 = threading.Thread(target=game, args=('飞车',))
# threads.append(t2)
#
# if __name__ == '__main__':
#     for t in threads:
#         # t.setDaemon(True)
#         t.start()
#
#     for t in threads:
#         t.join()
#     print('主线程运行结束')

# def func1(x):
#     x = random.randint(1,20)
#     sleep(x)
#     return x
#
#
# args = range(1, 10)
# # for i in args:
# #     res = func1(i)
# #     print(res)
# # a = ThreadPoolExecutor(max_workers=10)
# with ThreadPoolExecutor(max_workers=10) as executor:
#     # res = executor.map(func1, args)
#     res = [executor.submit(func1, i) for i in args]
#     print(res)
#     for i in as_completed(res):
#         print(i.result())

from threading import Thread
from datetime import datetime


class MyThread(Thread):
    """
    线程类，继承Thread, 调用start方法时，会调 run 方法，可在此写想要的逻辑

    python的threading.Thread类有一个run方法，用于定义线程的功能函数，可以在自己的线程类中覆盖该方法。
    而创建自己的线程实例后，通过Thread类的start方法，可以启动该线程，
    交给python虚拟机进行调度，当该线程获得执行的机会时，就会调用run方法执行线程。

    """

    def __init__(self, id, name):
        super().__init__()
        print("线程实例化")
        self.threadID = id
        self.name = name

    def run(self):
        print("线程启动")
        print("self.threadID:", self.threadID, ",self.name:", self.name)
        print(datetime.now(), "\n")


if __name__ == "__main__":
    threads = []
    for i in range(0, 10):
        t = MyThread(i, "线程" + str(i))
        threads.append(t)

    for t in threads:
        t.start()
        t.join()

    print("主线程结束，", datetime.now())

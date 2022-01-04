import threading
import time


def fun_1():
    print('开始')
    time.sleep(1)
    lock.acquire()
    print("第一道锁")
    fun_2()
    lock.release()


def fun_2():
    lock.acquire()
    print("第二道锁")
    lock.release()


if __name__ == '__main__':
    lock = threading.RLock()
    t1 = threading.Thread(target=fun_1)
    t2 = threading.Thread(target=fun_1)
    t1.start()
    t2.start()
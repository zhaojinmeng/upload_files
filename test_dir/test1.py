# -*- coding: utf-8 -*-

# @File    : test1.py
# @Date    : 2021-12-14
# @Author  : windyzhao

"""
0 0
1 1
2 3
3 5
4 8
5 12

1、1、2、3、5、8、13、21、34

n = (n-1)+ (n-2)
"""


def febonaqi(n):
    if n == 0:
        return n
    elif n == 1:
        return 1
    else:
        return febonaqi(n - 1) + febonaqi(n - 2)


class Fibs():
    def __init__(self, max):
        self.a = 0
        self.b = 1
        self.max = max

    def __iter__(self):
        return self

    def next(self):
        fib = self.a
        self.a, self.b = self.b, self.a + self.b
        if fib > self.max:
            raise StopIteration
        return fib


if __name__ == '__main__':
    # print(febonaqi(10))
    a = Fibs(10)

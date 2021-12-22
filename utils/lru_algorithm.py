# -*- coding: utf-8 -*-

# @File    : lru_algorithm.py
# @Date    : 2021-12-17
# @Author  : windyzhao
import collections

"""
算法题：LRU缓存机制

运用你所掌握的数据结构，设计和实现一个 LRU (最近最少使用) 缓存机制。它应该支持以下操作： 获取数据 get 和 写入数据 put 。

获取数据 get(key) - 如果关键字 (key) 存在于缓存中，则获取关键字的值（总是正数），否则返回 -1。

写入数据 put(key, value) - 如果关键字已经存在，则变更其数据值；如果关键字不存在，则插入该组「关键字/值」。

当缓存容量达到上限时，它应该在写入新数据之前删除最久未使用的数据值，从而为新的数据值留出空间。

进阶:

你是否可以在 O(1) 时间复杂度内完成这两种操作？

"""


class LRUAlgorithm(object):
    def __init__(self, length):
        self.order_dict = collections.OrderedDict()
        self.length = length  # 最长的限制
        self.now_length = 0  # 当前长度

    def get(self, key):
        value = self.order_dict.pop(key, None)
        if value is None:
            return -1

        self.order_dict[key] = value  # 放到头部

        return value

    def put(self, key, values):
        if self.now_length >= self.length:
            self.order_dict.popitem(last=False)  # 去掉最后一个（最先那个）

        value = self.order_dict.pop(key, False)

        self.order_dict[key] = value or values

        self.now_length += 1


if __name__ == '__main__':
    lru = LRUAlgorithm(length=3)
    print("a:{}".format(lru.get("a")))
    print("=============")
    lru.put("a", 1)
    lru.put("b", 2)
    lru.put("c", 3)
    lru.put("d", 4)
    lru.put("e", 5)
    print("=============")
    print("a:{}".format(lru.get("a")))
    print("b:{}".format(lru.get("b")))
    print("c:{}".format(lru.get("c")))
    print("d:{}".format(lru.get("d")))
    print("e:{}".format(lru.get("e")))
    print("c:{}".format(lru.get("c")))
    print("============")
    print(lru.order_dict)

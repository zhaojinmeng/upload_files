# -*- coding: utf-8 -*-

# @File    : redis_test.py
# @Date    : 2021-12-22
# @Author  : windyzhao
import redis

r = redis.Redis(host='192.168.165.195', port=6379, password="kwQ1gLz6kUaY", decode_responses=True, db=2)
print("===")

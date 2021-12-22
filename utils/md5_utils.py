# -*- coding: utf-8 -*-

# @File    : md5_utils.py
# @Date    : 2021-12-14
# @Author  : windyzhao
import hashlib


def make_md5(content):
    """
    生成md5码
    """
    if not isinstance(content, bytes):
        content = content.encode()

    md5hash = hashlib.md5(content)
    md5 = md5hash.hexdigest()
    return md5

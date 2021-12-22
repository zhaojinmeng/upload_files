# -*- coding: utf-8 -*-

# @File    : path_utils.py
# @Date    : 2021-12-14
# @Author  : windyzhao
import os
import re
from django.conf import settings


def make_user_path(username, base_path):
    return os.path.join(base_path, username)


def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_chunk_info(username, identifier):
    info = {}
    make_dir(settings.MEDIA_ROOT)  # /Users/windyzhao/windy_projects/django_project/upload_file_demo/static/ 存放文件根路径
    path = make_user_path(username, settings.MEDIA_ROOT)
    make_dir(path)  # /Users/windyzhao/windy_projects/django_project/upload_file_demo/static/admin_1/ 具体用户的文件路径
    md5_path = os.path.join(path, identifier)
    make_dir(md5_path)  # /static/admin_1/b6c5bec42f652b0e7b08ab03bb45c7f8/   当前上传文件的路径
    file_path = os.path.join(md5_path, "files")
    make_dir(file_path)  # /static/admin_1/b6c5bec42f652b0e7b08ab03bb45c7f8/files/  合并完整的存放文件路径
    chunk_path = os.path.join(md5_path, "chunk")
    make_dir(chunk_path)  # /static/admin_1/b6c5bec42f652b0e7b08ab03bb45c7f8/chunk/  分片文件存放路径

    info['file_path'] = file_path
    info['chunk_path'] = chunk_path

    return info


def get_files_type(filename):
    """
    文件类型校验
    """
    file_type = re.match(r'.*\.(txt|doc|docx|pdf|exe|zip|rar|tar|xlsx|pptx|dmg|mp4|mp3)', filename)
    return file_type


def merge_files(chunk_path, file_name, file_path):
    """
    chunk_path:分片文件存放的位置
    file_name：合并后的文件名称
    file_path：合并后文件存放的位置
    """
    chunk_paths = os.listdir(chunk_path)
    chunk_path_dict = {int(i.split("_")[-1]): i for i in chunk_paths}
    chunk_path_list = sorted(chunk_path_dict.items(), key=lambda item: item[0])  # 排序,或者直接读数据库排序

    with open(os.path.join(file_path, file_name), "wb") as fp:

        for _, split_file_name in chunk_path_list:

            split_path = os.path.join(chunk_path, split_file_name)
            if not os.path.isfile(split_path):
                continue

            with open(split_path, "rb") as sf:
                fp.write(sf.read())

    # 删除掉文件
    for chunk_file_name in chunk_paths:
        try:
            os.remove(os.path.join(chunk_path, chunk_file_name))
        except BaseException as e:
            print("delete file error:{}".format(e))

    # 删除掉文件夹
    os.removedirs(chunk_path)

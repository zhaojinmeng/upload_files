# -*- coding: utf-8 -*-

# @File    : serializer.py
# @Date    : 2021-12-15
# @Author  : windyzhao
from rest_framework import serializers

from app1.models import UploadInfo, CheckInfo


class UploadInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadInfo
        fields = "__all__"


class CheckInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInfo
        fields = "__all__"

# -*- coding: utf-8 -*-

# @File    : urls.py
# @Date    : 2021-12-11
# @Author  : windyzhao

from django.conf.urls import url
from .views import upload_file, UploadAPIView, merge_files  # UploadModelViewSet
from rest_framework.routers import SimpleRouter

urlpatterns = [
    url(r"^upload/$", upload_file),
    url(r"^merge_files/$", merge_files),
    url('^upload_file/$', UploadAPIView.as_view(), name='globalUpload'),

]

# routers = SimpleRouter()
# routers.register(r"upload_file_set", UploadModelViewSet, basename="upload")
#
# urlpatterns += routers.urls

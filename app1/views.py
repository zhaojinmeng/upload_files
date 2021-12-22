import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view

from app1.models import UploadInfo, CheckInfo
from utils.path_utils import get_chunk_info, get_files_type
from utils.path_utils import merge_files as utils_merge_files
from app1.serializer import UploadInfoModelSerializer, CheckInfoModelSerializer
from django.db import transaction


def upload_file(request):
    return JsonResponse(data={"result": True})


@api_view(["POST"])
def merge_files(request):
    params = request.data
    file_name = params["filename"]
    md5 = params["identifier"]

    upload_obj = UploadInfo.objects.filter(md5=md5).first()
    if upload_obj is None:
        return Response(data={"result": False, "message": "上传失败，分片数据被删除"})

    chunk_path = upload_obj.chunk_path
    file_path = upload_obj.path

    utils_merge_files(chunk_path=chunk_path, file_name=file_name, file_path=file_path)

    return Response(data={"result": True})


class UploadAPIView(APIView):

    def __init__(self, *args, **kwargs):
        super(UploadAPIView, self).__init__(*args, **kwargs)
        self.unique_user = "admin_1"

    def get(self, request, *args, **kwargs):
        params = request.GET
        filename = params["filename"]  # 文件名称
        identifier = params['identifier']  # 文件唯一标识

        # 检测上传文件是否存在
        if not filename:
            return Response(data={"msg": "请选择要上传的文件"})

        # 上传文件类型检测
        file_type = get_files_type(filename)
        if not file_type:
            return Response(data={"msg": "文件类型不匹配, 请重新上传"})

        md5 = params['identifier']  # 文件md5
        size = params['totalSize']  # 文件大小
        total_chunk = params['totalChunks']  # 总分片

        # 根据文件MD5和文件大小查询数据库文件是否已经上传, 若存在则返回标志完成秒传
        upload_obj = UploadInfo.get_object(md5=md5)
        if upload_obj is None:
            file_info = get_chunk_info(params.get("unique_user", self.unique_user), identifier)  # 生成此用户唯一的文件夹名称

            # 未上传过
            UploadInfo.objects.create(name=filename, chunk_path=file_info["chunk_path"], md5=md5,
                                      size=size, total_chunks=int(total_chunk), path=file_info["file_path"])

            return Response(data={"result": True})

        # 断点续传: 查询已经上传的分片, 将已经上传的分片以数组的形式返回给前台
        uploaded_list = CheckInfo.objects.filter(md5=identifier).values_list("chunk_number", flat=True)

        if len(uploaded_list) == int(total_chunk):
            file_info = get_chunk_info(params.get("unique_user", self.unique_user), identifier)  # 生成此用户唯一的文件夹名称

            if os.path.exists(os.path.join(file_info["file_path"], filename)):
                # 秒传，本地已经存在此数据
                return Response(data={"isExist": True})
            else:
                # 传递完毕，但是未合并文件
                return Response(data={"code": 0, "merge": True})

        return Response(data={"result": True, "uploaded": list(uploaded_list)})

    @csrf_exempt
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        params = request.POST
        filename = params["filename"]
        identifier = params['identifier']  # 文件唯一标识
        chunk_number = params["chunkNumber"]  # 当前的顺序
        total_chunks = params["totalChunks"]  # 当前的顺序

        file = request.FILES.get('file')

        # 上传文件类型检测
        file_type_bool = get_files_type(filename)
        if not file_type_bool:
            return Response(data={"msg": "文件类型不匹配, 请重新上传"})

        upload_info = UploadInfo.objects.filter(md5=identifier).first()
        if upload_info is None:
            return Response(data={"result": False, "meg": "先请求确认文件是否存可以秒传！"})

        dir_path = upload_info.chunk_path  # 文件夹路径
        file_name = "{}_{}".format(identifier, chunk_number)
        file_path = os.path.join(dir_path, file_name)

        sid = transaction.savepoint()

        try:
            _, is_create = CheckInfo.objects.get_or_create(md5=identifier, chunk_number=int(chunk_number),
                                                           defaults={"md5": identifier, "name": file_name,
                                                                     "chunk_number": int(chunk_number),
                                                                     "path": file_path})
            if not is_create:
                return Response(data={"result": True})

            with open(file_path, "wb") as w:
                # w.write(file.read())
                for chunk in file.chunks():
                    w.write(chunk)

        except BaseException as e:
            print("error:{}".format(e))
            transaction.savepoint_rollback(sid)

        if chunk_number == total_chunks:
            print("调用合并")
            return Response(data={"code": 0, "merge": True})

        return Response(data={"result": True})

# class UploadModelViewSet(ModelViewSet):
#     serializer_class = UploadInfoModelSerializer
#     queryset = UploadInfo.objects.all().order_by("-id")
#
#     def __init__(self, *args, **kwargs):
#         super(UploadModelViewSet, self).__init__(*args, **kwargs)
#         self.unique_user = "admin_1"
#
#     @action(methods=["post"], detail=False)
#     def merge_files(self, request, *args, **kwargs):
#         params = request.data
#         print(params)  # path, file_name, file_path
#
#         # utils_merge_files()
#
#         return Response(data={"result": True})
#
#     @action(methods=["get"], detail=False)
#     def get_files(self, request, *args, **kwargs):
#         return Response(data={"result": "get_files_get"})
#
#     @action(methods=["post"], detail=False)
#     def get_files(self, request, *args, **kwargs):
#         return Response(data={"result": "get_files_post"})
#
#     # def list(self, request, *args, **kwargs):
#     #     print("--")
#     #     return self.list(self, request, *args, **kwargs)
#
#     # def get(self, request, *args, **kwargs):
#     #     params = request.GET
#     #     filename = params.get("filename", False)  # 文件名称
#     #
#     #     # 检测上传文件是否存在
#     #     if not filename:
#     #         return Response(data={"msg": "请选择要上传的文件"})
#     #
#     #     # 上传文件类型检测
#     #     file_type = get_files_type(filename)
#     #     if not file_type:
#     #         return Response(data={"msg": "文件类型不匹配, 请重新上传"})
#     #
#     #     md5 = params['identifier']  # 文件md5
#     #     size = params['totalSize']  # 文件大小
#     #
#     #     # 根据文件MD5和文件大小查询数据库文件是否已经上传, 若存在则返回标志完成秒传
#     #     upload_obj = UploadInfo.get_object(md5=md5, size=size, name=filename)
#     #     if upload_obj is None:
#     #         file_info = get_chunk_info(params.get("unique_user", self.unique_user), filename)  # 生成此用户唯一的文件夹名称
#     #
#     #         # 未上传过
#     #         upload_info = UploadInfo.objects.create(
#     #             **{"name": filename, "path": file_info["chunk_path"], "md5": md5, "size": size})
#     #
#     #         return Response(data={"result": True, "upload_info_id": upload_info.id})
#     #
#     #     if upload_obj.upload_finish:
#     #         return Response(data={"skipUpload": True})
#     #
#     #     # 断点续传: 查询已经上传的分片, 将已经上传的分片以数组的形式返回给前台
#     #     uploaded_list = [i.md5 for i in upload_obj.checkinfo_set.all()]
#     #     return Response(data={"result": True, "uploaded": uploaded_list})
#     #
#     # @csrf_exempt
#     # def post(self, request, *args, **kwargs):
#     #     params = request.POST
#     #     name = params["name"]
#     #     md5 = params["md5"]
#     #     size = params["size"]
#     #     chunk_number = params["chunkNumber"]
#     #     upload_info_id = params["upload_info_id"]
#     #
#     #     file = request.FILES.get('file')
#     #
#     #     # 上传文件类型检测
#     #     # file_type = get_files_type(name)
#     #     # if not file_type:
#     #     #     return Response(data={"msg": "文件类型不匹配, 请重新上传"})
#     #
#     #     # 存储目录不存在则创建
#     #     upload_info = UploadInfo.objects.filter(id=upload_info_id).first()  # 生成此用户唯一的文件夹名称
#     #     if upload_info is None:
#     #         return Response(data={"result": False, "meg": "现请求get请求确认文件信息！"})
#     #
#     #     dir_path = upload_info.path  # 文件夹路径
#     #     file_name = "{}_{}".format(params["chunkNumber"], params["identifier"])
#     #     file_path = os.path.join(dir_path, file_name)
#     #
#     #     # 打开特定的文件进行二进制的写操作
#     #     with open(file_path, "wb") as w:
#     #         for chunk in file.chunks():
#     #             w.write(chunk)
#     #
#     #     CheckInfo.objects.create(md5=md5, name=file_name, path=file_path, upload_info=upload_info)
#     #
#     #     return Response(data={"needMerge": True, "timeStamp": time.time()})

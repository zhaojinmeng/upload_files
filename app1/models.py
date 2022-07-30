from django.db import models


# Create your models here.

class UploadInfo(models.Model):
    name = models.CharField(max_length=128, verbose_name="文件名称")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    md5 = models.CharField(max_length=255, default='', verbose_name="md5值")
    size = models.CharField(max_length=32, default=0, verbose_name="文件大小")
    upload_finish = models.BooleanField(default=False, verbose_name="文件是否完整生成完成")
    total_chunks = models.IntegerField(verbose_name="总的分片数")
    path = models.CharField(max_length=255, verbose_name="完整文件存放路径")
    chunk_path = models.CharField(max_length=255, verbose_name="分片文件存放路径")

    class Meta:
        verbose_name = "上传文件信息"

    @classmethod
    def get_object(cls, md5):
        data = UploadInfo.objects.filter(md5=md5).first()
        return data


class CheckInfo(models.Model):
    md5 = models.CharField(max_length=128, default='', verbose_name="md5值")
    chunk_number = models.IntegerField(default=-1, verbose_name="第几个分片")
    name = models.CharField(max_length=255, verbose_name="文件名称")
    path = models.CharField(max_length=255, verbose_name="路径")
    check_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "校验文件信息"

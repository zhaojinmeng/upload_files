#### 大文件的分片上传，断点续传，秒传，暂停/开始上传

##### 使用场景：

​		用户上传大文件，如几百M的视频，几个G的文件等。使用常规的HTTP一次传输的话，大文件会存在超时的情况，速度慢，且容易断开。所以针对此业务场景，普遍的解决方式就是文件的分片上传，断点续传。

##### 分片上传：

​		分片上传的原理就是在前端将文件分片，然后一片一片的传给服务端，由服务端对分片的文件进行合并，从而完成大文件的上传。分片上传可以解决文件上传过程中超时、传输中断造成的上传失败，而且一旦上传失败后，已经上传的分片不用再次上传，不用重新上传整个文件，因此采用分片上传可以实现断点续传以及跨浏览器上传文件。

##### 断点续传：

​		断点续传是分片上传时，若已经上传过部分分片，那么后端返回已经上传过的分片信息，前端只用传为上传的分片即可。

##### 秒传：

​		如服务器已经存在要上传的文件，那么就不必要再上传一次。这就是秒传。

##### 暂停/开始：

​		所谓的暂停上传，就是暂停为上传的分片文件，而不是暂停正在上传中的请求。开始上传就是把暂停后未上传的文件上传到后端。



##### 使用的前后端技术栈：

​			1.前端 `vue`，使用组件`vue-simple-uploader`

​			2.后端`python`，使用框架`django`

##### 实现难点：

​		难点主要在前端，前端需要计算上传文件的唯一标识，使用md5计算。还需要对文件进行分片。每次传输时都带上文件的唯一标识，后端把分片信息按照文件的唯一标识存储起来。当前端传输完成后，后端再把分片文件，按照分片顺序写成一个完整的文件。

##### 实现过程：

​		1.前端进行文件的md5的计算，对文件进行分片，每次http传输都带上文件的唯一md5标识和分片文件，后端存储分片数据。

​		2.前端上传完成全部的分片，后端按照分片顺序写好文件，若写入成功，那么上传成功，写入失败，上传失败。



##### 流程：



![大文件上传流程](https://github.com/zhaojinmeng/upload_files/blob/master/utils/%E5%A4%A7%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E6%B5%81%E7%A8%8B.png)



##### 启动前端：

文件路径: ui/fast-uploader

命令：

```shell
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

##### 启动后端：

```python
# 1.配置setting的数据库
# 2.python manage.py makemigrations
# 3.python manage.py migrate
# 4.python manage.py runserver
```

#### 前端页面体验路径
```js
/breakpoint
/md5
/skip
/chunk
```
每个页面的功能不一样

##### 文件存储路径：

`upload_file_demo/static'`下。

##### github地址：

完整项目：https://github.com/zhaojinmeng/upload_files/tree/master

##### 参考文档：

1.vue-simple-uploader组件：https://github.com/simple-uploader/vue-uploader/blob/master/README_zh-CN.md

2.Uploader组件：https://github.com/simple-uploader/Uploader/blob/develop/README_zh-CN.md#%E9%85%8D%E7%BD%AE

3.博客参考：https://www.helloweba.net/javascript/632.html

4.前端来源：https://github.com/lrfbeyond/fast-uploader

若本项目侵权，请联系我删除，谢谢！






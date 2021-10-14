

####  介绍

基于百度飞桨paddleocr截屏文字识别

#### 可执行程序

[main.exe](https://pan.baidu.com/s/1lF3f9rVa5z_zQpWcqI-NoQ )

链接：https://pan.baidu.com/s/1lF3f9rVa5z_zQpWcqI-NoQ 
提取码：d4b7

#### Pyinstaller打包

修改 paddle\dataset\image.py源码，删除部分代码，屏蔽subprocess调用

```
# if six.PY3:
#     import subprocess
#     import sys
#     import_cv2_proc = subprocess.Popen(
#         [sys.executable, "-c", "import cv2"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE)
#     out, err = import_cv2_proc.communicate()
#     retcode = import_cv2_proc.poll()
#     if retcode != 0:
#         cv2 = None
#     else:
#         import cv2
# else:
#     try:
#         import cv2
#     except ImportError:
#         cv2 = None
try:
    import cv2
except ImportError:
    cv2 = None
```

修改main.spec 【pathex、  binaries 与 datas中的路径地址】

```
pyinstaller main.spec 
```



参考：

- 通过截屏快速实现图片转文字、图片转表格  https://gitee.com/lazytech_group/scr2txt
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
解决mac下解压zip文件乱码问题

代码参考:
http://stackoverflow.com/questions/9431918/extracting-zip-file-contents-to-specific-directory-in-python-2-7
http://www.zhihu.com/question/20523036/answer/35225920
http://stackoverflow.com/questions/4917284/extract-files-from-zip-without-keeping-the-structure-using-python-zipfile
"""
import sys
import os.path
import zipfile

zip_file_name = sys.argv[1]
if not zip_file_name.endswith('.zip'):
    print '文件名需要zip结尾'

# 解压到文件名的同名文件夹
target_root_path = zip_file_name[:-4]
if not os.path.exists(target_root_path):
    print '创建目录'
    os.makedirs(target_root_path)

fh = open(zip_file_name, 'rb')
zip_file = zipfile.ZipFile(fh)
for name in zip_file.namelist():
    # fix mac 下乱码
    unicode_name = name.decode('gbk')
    file_name = os.path.basename(unicode_name)

    if not file_name:
        continue

    target_name = os.path.join(target_root_path, unicode_name)
    target_path = os.path.dirname(target_name)
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    print u'解压到: {0}'.format(target_name)

    data = zip_file.read(name)
    with open(target_name, 'wb') as f:
        f.write(data)

fh.close()

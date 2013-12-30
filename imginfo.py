#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from PIL import Image


def get_imginfo(img):
    lis = []
    lis.append('大小：%spx * %spx' % img.size)
    return lis

def get_imginfo_by_path(s):
    img = Image.open(s)
    lis = []
    path = os.path.split(s)[0] or os.getcwd()
    name = os.path.split(s)[1] or s
    lis.append('路径：%s' % path)
    lis.append('文件名：%s' % name)
    lis.extend(get_imginfo(img))
    return lis


if __name__ == '__main__':
    for item in get_imginfo_by_path('1.jpg'):
        print item
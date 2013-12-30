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

def ispic(f):
    if os.path.isfile(f):
        return os.path.splitext(f)[1].upper() in ['.PNG', '.JPG', '.JPEG', '.GIF', '.BMP']
    else:
        return False

def get_all_imgs(path):
    imgs = []
    dirs = [path]
    dirs.extend(os.path.join(path, dir) for dir in filter(os.path.isdir, os.listdir(path)))
    for dir in dirs:
        imgs.extend(filter(ispic, [os.path.join(dir, d) for d in os.listdir(dir)]))
    return imgs
    

if __name__ == '__main__':
    path = '/Users/windrunner/imgdedupl'
    for item in get_all_imgs(path):
        print item

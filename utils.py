#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from PIL import Image


SPLIT_PARTS = 4


def make_regular_image(image1, image2):
    return image2.resize(image1.size).convert('RGB')


def split_image(image):
    w, h = image.size
    pw, ph = w/SPLIT_PARTS, h/SPLIT_PARTS
    try:
        assert w % pw == 0
    except AssertionError:
        w = pw * SPLIT_PARTS
    try:
        assert h % ph == 0
    except AssertionError:
        h = ph * SPLIT_PARTS
    return [image.crop((i, j, i+pw, j+ph)).copy()
            for i in xrange(0, w, pw)
            for j in xrange(0, h, ph)]


def hist_similar(lh, rh):
    return sum(1 - (0 if left == right else float(abs(left - right))/max(left, right))
               for left, right in zip(lh, rh))/len(lh)


def calc_similar(li, ri):
    return sum(hist_similar(left.histogram(), right.histogram())
               for left, right in zip(split_image(li), split_image(ri))) / SPLIT_PARTS**2


def calc_similar_by_path(lf, rf):
    li, ri = Image.open(lf), Image.open(rf)
    ri = make_regular_image(li, ri)
    return calc_similar(li, ri)


def get_similar_list(lis):
    similar_list = [[image] for image in lis]
    length = len(lis)
    for i in range(length-1, -1, -1):
        for j in range(i):
            if len(similar_list[i]) > 1:
                break
            if calc_similar_by_path(similar_list[i][0], similar_list[j][0]) > 0.7:
                similar_list[j].extend(similar_list[i])
                break
    similar_list = filter(lambda similar_images: len(similar_images) > 1, similar_list)
    return similar_list


def get_image_info(image):
    lis = list()
    lis.append('大小：%spx * %spx' % image.size)
    return lis


def get_image_info_by_path(s):
    image = Image.open(s)
    lis = []
    path = os.path.split(s)[0] or os.getcwd()
    name = os.path.split(s)[1] or s
    lis.append('路径：%s' % path)
    lis.append('文件名：%s' % name)
    lis.extend(get_image_info(image))
    return lis


def is_image(f):
    if os.path.isfile(f):
        return os.path.splitext(f)[1].upper() in ['.PNG', '.JPG', '.JPEG', '.GIF', '.BMP']
    else:
        return False


def get_all_images(path):
    images = []
    dirs = [path]
    for directory in dirs:
        images.extend(filter(is_image, [os.path.join(p, f)
                                        for p, _, files in os.walk(directory)
                                        for f in files]))
    return images
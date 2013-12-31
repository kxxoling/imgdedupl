#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from PIL import Image


SPLIT_PARTS = 4


def make_regalur_image(img1, img2):
    return img2.resize(img1.size).convert('RGB')

def split_image(img):
    w, h = img.size
    pw, ph = w/SPLIT_PARTS, h/SPLIT_PARTS
    try:
        assert w % pw == 0
    except:
        w = pw * SPLIT_PARTS
    try:
        assert h % ph ==0
    except:
        h = ph * SPLIT_PARTS
    return [img.crop((i, j, i+pw, j+ph)).copy() \
                for i in xrange(0, w, pw) \
                for j in xrange(0, h, ph)]

def hist_similar(lh, rh):
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def calc_similar(li, ri):
    return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / SPLIT_PARTS**2

def calc_similar_by_path(lf, rf):
    li, ri = Image.open(lf), Image.open(rf)
    ri = make_regalur_image(li, ri)
    return calc_similar(li, ri)

def get_similar_list(lis):
    lislist = [[item] for item in lis]
    length = len(lis)
    for i in range(length-1, -1, -1):
        for j in range(i):
            if len(lislist[i]) > 1:
                break
            if calc_similar_by_path(lislist[i][0], lislist[j][0]) > 0.7:
                lislist[j].extend(lislist[i])
                break
    lislist = filter(lambda lis:len(lis)>1 ,lislist)
    return lislist

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
    path = '/Users/windrunner/Downloads/googled'
    for item in get_all_imgs(path):
        print item
        img1 = '1.jpg'
    img2 = '2.png'
    print 'Similarity between %s and %s is %s' % (img1, img2, str(100*calc_similar_by_path(img1, img2))+'%')
    path = '/Users/windrunner/imgdedupl'
    lis = get_all_imgs(path)
    lislist = get_similar_list(lis)

    for l in lislist:
        print l

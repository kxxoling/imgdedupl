#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image


SPLIT_PARTS = 10

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
	assert len(lh) == len(rh)
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def calc_similar(li, ri):
	return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / SPLIT_PARTS**2

def calc_similar_by_path(lf, rf):
	li, ri = Image.open(lf), Image.open(rf)
	ri = make_regalur_image(li, ri)
	return calc_similar(li, ri)
	

if __name__ == '__main__':
	img1 = '1.jpg'
	img2 = '2.png'
	print 'Similarity between %s and %s is %s' % (img1, img2, str(100*calc_similar_by_path(img1, img2))+'%')

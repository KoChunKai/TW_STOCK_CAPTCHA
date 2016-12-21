# -*- coding: utf8 -*-
# coding: utf8

import matplotlib

matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import glob
from PIL import Image,ImageDraw
from PIL import ImageFilter
from PIL import ImageEnhance
import shutil
import time

def getCaptcha(im):
	image = cv2.imread(im)
	# plt.imshow(image)

	kernel = np.ones((4,4), np.uint8)
	erosion = cv2.erode(image, kernel)
	blurred = cv2.GaussianBlur(erosion, (5, 5), 0)
	edged = cv2.Canny(blurred, 30, 150)
	dilation = cv2.dilate(edged, kernel)

	image , contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key = lambda x : x[1])

	ary = []
	for (c, _) in cnts:
		(x, y, w, h) = cv2.boundingRect(c)
		if w > 15 and h > 15:
			ary.append((x, y, w, h))

	# fig = plt.figure()
	data = []
	for id, (x, y, w, h) in enumerate(ary):
		roi = dilation[y: y + h, x: x + w]
		thresh = roi.copy()
		# a = fig.add_subplot(1, len(ary), id+1)
		res = cv2.resize(thresh, (50,50))
		data.append(res)
	return data

def calImage(im):
	image = cv2.imread(im)
	# plt.imshow(image)

	kernel = np.ones((4,4), np.uint8)
	erosion = cv2.erode(image, kernel)
	blurred = cv2.GaussianBlur(erosion, (5, 5), 0)
	edged = cv2.Canny(blurred, 30, 150)
	dilation = cv2.dilate(edged, kernel)

	image , contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key = lambda x : x[1])

	ary = []
	for (c, _) in cnts:
		(x, y, w, h) = cv2.boundingRect(c)
		if w > 15 and h > 15:
			ary.append((x, y, w, h))

	# fig = plt.figure()

	for id, (x, y, w, h) in enumerate(ary):
		roi = dilation[y: y + h, x: x + w]
		thresh = roi.copy()
		# a = fig.add_subplot(1, len(ary), id+1)
		res = cv2.resize(thresh, (50,50))
		return res

def mse(imgA, imgB):
	try:
		err = np.sum((imgA.astype("float") - imgB.astype("float")) ** 2)
		err /= float(imgA.shape[0] * imgA.shape[1])
		return err
	except Exception, e:
		return 999999999

def getNumber(pic):
	min_a = 999999999
	min_png = None
	path = os.getcwd()+'/sort'
	for directory in os.listdir(path):
		if directory != '.DS_Store':
			data = glob.glob(path + "/" + directory +'/*.jpg')
			for filePath in data:
				ref = calImage(filePath)
				v = mse(ref, pic)
				if v < min_a:
					min_png = directory
					min_a = v
				# time.sleep(0.01)
				# print str(directory) + '\t' + str(min_a) +'\t' + str(min_png)
				if(min_a < 3000):
					return min_png
	return min_png

def segment(im):
	im_new = []
	x1 = 10
	y1 = 5
	x2 = 45
	y2 = 50
	next = 40
	for i in range(5):
		im1 = im.crop((x1, y1, x2, y2))
		x1 = x1 + next
		x2 = x2 + next
		im_new.append(im1)
	return im_new

def imgTransfer(img):
	im = img
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(1)
	im = im.convert('L')
	return im

def cutPictures(img):
	im = imgTransfer(img)
	pics = segment(im)
	return pics

data = glob.glob(os.getcwd()+'/sample1/*.jpg')
for path in data:
	images = cutPictures(Image.open(path))
	result = []
	for image in images:
		# i = str(int(time.time()))
		image.save(os.getcwd() + '/cut/' + 'i' + '.jpg', 'jpeg')
		# time.sleep(1)
		result.append(getNumber(calImage(os.getcwd() + '/cut/' + 'i' + '.jpg')))
	print result
	# break



# print getNumber(calImage(os.getcwd() + '/cut/1482200524.jpg'))

# data = glob.glob(os.getcwd()+'/cut/*.jpg')
# for path in data:
# 	result = []
# 	# print path
# 	# image = getCaptcha(path)
# 	# for im in image:

# 	result.append(getNumber(calImage(path)))
# 	print result
# data = glob.glob(os.getcwd()+'/cut/*.jpg')
# for path in data:
# 	rs = getNumber(calImage(path))
# 	if not os.path.exists(os.getcwd()+'/sort/'+ rs):
# 		print "None:" + rs
# 	else:
# 		print path.replace("cut/", "sort/" + rs + '/')
# 		# os.rename(path, path.replace("cut/", "sort/" + rs.lower() + '/'))
# 		shutil.move(path, path.replace("cut/", "sort/" + rs.lower() + '/'))



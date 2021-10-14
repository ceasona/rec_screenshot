#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021.2.25
# @Author  : Joran
# @FileName: screenshot.py
# @Blog    ：

import cv2
import os

import numpy
from PIL import ImageGrab
import time
import paddleocr

ocrer = paddleocr.PaddleOCR()


# 截图
def cut():
    global img
    scrren_cut()
    img = cv2.imread('screen.jpg')
    os.remove('screen.jpg')
    # print(type(img))
    # exit(2)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', on_mouse)
    cv2.imshow('image', img)
    cv2.waitKey(0)



def scrren_cut():
    beg = time.time()
    debug = False
    image = ImageGrab.grab()
    # image2 = numpy.array(image)

    image.save("screen.jpg")
    # PIL image to OpenCV image


def on_mouse(event, x, y, flags, param):
    global img, point1, point2
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        point1 = (x, y)
        cv2.circle(img2, point1, 10, (0, 255, 0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
        cv2.rectangle(img2, point1, (x, y), (255, 0, 0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
        point2 = (x, y)
        cv2.rectangle(img2, point1, point2, (0, 0, 255), 5)
        cv2.imshow('image', img2)
        min_x = min(point1[0], point2[0])
        min_y = min(point1[1], point2[1])
        width = abs(point1[0] - point2[0])
        height = abs(point1[1] - point2[1])
        cut_img = img[min_y:min_y + height, min_x:min_x + width]
        # cv2.imwrite("{0}.jpg".format("111"), cut_img)

        word_mes = ocrer.ocr(cut_img, det=True, rec=True, cls=False)
        print("#" * 12)
        res = []
        for i in word_mes:
            # print(i[-1][0])
            res.append(i[-1][0])
        res = ' '.join(res)
        print(res)
        exit(0)


if __name__ == "__main__":
    cut()
    # for i in range(1,101):
    #     cut()
    #     time.sleep(0.5)

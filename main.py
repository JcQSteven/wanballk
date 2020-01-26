#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/25 7:18 PM
# @Author  : 573v3n
# @Contact : 523348709@qq.com
# @Site    : 
# @File    : main.py
# @Software: PyCharm
import colorsys
import cv2
import numpy as np
import collections
import os
import time

def canConnect(x1,y1,x2,y2,imageMatrix):
    '''
        :两个方块是否可以连通函数
        '''
    # 将传入的二维数组赋值给本地全局变量，

    result = imageMatrix
    # 如果有一个为0 直接返回False
    if result[x1][y1] == 0 or result[x2][y2] == 0:
        return False
    if x1 == x2 and y1 == y2:
        return False
    if result[x1][y1] != result[x2][y2]:
        return False
    # 先判断横向可连通
    if horizontalCheck(x1, y1, x2, y2,result):
        return True
    # 在判断纵向可连通
    if verticalCheck(x1, y1, x2, y2,result):
        return True
    # 判断一个拐点的可连通情况
    if turnOnceCheck(x1, y1, x2, y2,result):
        return True
    # 判断两个拐点的可连通情况
    if turnTwiceCheck(x1, y1, x2, y2,result):
        return True
    # 都不可连通，返回false
    return False

def horizontalCheck(x1,y1,x2,y2,result):
    '''
    :判断水平方向能够连通
    '''

    # 判断两个不是同一个方块
    if x1 == x2 and y1 == y2:

        return False
    # 判断两个的纵坐标相同
    if x1 != x2:
        return False
    startY = min(y1, y2)
    endY = max(y1, y2)
    # 判断两个方块是否相邻
    if (endY - startY) == 1:
        return True
    # 判断两个方块通路上是否都是0，有一个不是，就说明不能联通，返回false
    for i in range(startY+1,endY):
        if result[x1][i] != 0:
            return False
    return True


def verticalCheck(x1,y1,x2,y2,result):
    '''
    :判断垂直方向能否连通
    '''
    # 判断不是同一个方块
    if x1 == x2 and y1 == y2:
        return False
    # 判断两个横坐标相同
    if y1 != y2:
        return False
    startX = min(x1, x2)
    endX = max(x1, x2)
    # 判断两个方块是否相邻
    if (endX - startX) == 1:
        return True
    # 判断两方块儿通路上是否可连。
    for i in range(startX+1,endX):
        if result[i][y1] != 0:
            return False
    return True


def turnOnceCheck(x1,y1,x2,y2,result):
    '''
    :判断单拐点情况能否连通
    '''
    # 实现单拐点校验。
    if x1 == x2 and y1 == y2:
        return False
    # 一个拐点，说明两个方块必须在不同行不同列！
    if x1 != x2 and y1 != y2:
        # cx cy dx dy 记录两个拐点的坐标
        cx = x1
        cy = y2
        dx = x2
        dy = y1
        # 拐点为空，从第一个点到拐点并且从拐点到第二个点可通，则整条路可通。
        if result[cx][cy] == 0:
            if horizontalCheck(x1, y1, cx, cy,result) and verticalCheck(cx, cy, x2, y2,result):
                return True
        if result[dx][dy] == 0:
            if verticalCheck(x1, y1, dx, dy,result) and horizontalCheck(dx, dy, x2, y2,result):
                return True
    return False


def turnTwiceCheck(x1,y1,x2,y2,result):
    '''
    :两个拐点的情况能否连通
    '''
    if x1 == x2 and y1 == y2:
        return False
    # 遍历整个数组找合适的拐点
    for i in range(0,len(result)):
        for j in range(0,len(result[1])):
            # 不为空不能作为拐点
            if result[i][j] != 0:
                continue
            # 不和被选方块在同一行列的
            # 不能作为拐点
            if i != x1 and i != x2 and j != y1 and j != y2:
                continue
            # 作为交点的部分也要过滤掉
            if (i == x1 and j == y2) or (i == x2 and j == y1):
                continue
            if turnOnceCheck(x1, y1, i, j,result) and (horizontalCheck(i, j, x2, y2,result) or verticalCheck(i, j, x2, y2,result)):
                return True
            if turnOnceCheck(i, j, x2, y2,result) and (horizontalCheck(x1, y1, i, j,result) or verticalCheck(x1, y1, i, j,result)):
                return True

    return False

def getColorList():
    dict = collections.defaultdict(list)

    # 黑色
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 46])
    color_list = []
    color_list.append(lower_black)
    color_list.append(upper_black)
    dict['black'] = color_list

    # #灰色
    # lower_gray = np.array([0, 0, 46])
    # upper_gray = np.array([180, 43, 220])
    # color_list = []
    # color_list.append(lower_gray)
    # color_list.append(upper_gray)
    # dict['gray']=color_list

    # 白色
    lower_white = np.array([0, 0, 221])
    upper_white = np.array([180, 30, 255])
    color_list = []
    color_list.append(lower_white)
    color_list.append(upper_white)
    dict['white'] = color_list

    # 红色
    lower_red = np.array([156, 43, 46])
    upper_red = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['red'] = color_list

    # 红色2
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['red2'] = color_list

    # 橙色
    lower_orange = np.array([11, 43, 46])
    upper_orange = np.array([19, 255, 255])
    color_list = []
    color_list.append(lower_orange)
    color_list.append(upper_orange)
    dict['orange'] = color_list

    # 黄色
    lower_yellow = np.array([20, 43, 46])
    upper_yellow = np.array([34, 255, 255])
    color_list = []
    color_list.append(lower_yellow)
    color_list.append(upper_yellow)
    dict['yellow'] = color_list

    # 绿色
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    color_list = []
    color_list.append(lower_green)
    color_list.append(upper_green)
    dict['green'] = color_list

    # 青色
    lower_cyan = np.array([78, 43, 46])
    upper_cyan = np.array([99, 255, 255])
    color_list = []
    color_list.append(lower_cyan)
    color_list.append(upper_cyan)
    dict['cyan'] = color_list

    # 蓝色
    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])
    color_list = []
    color_list.append(lower_blue)
    color_list.append(upper_blue)
    dict['blue'] = color_list

    # 紫色
    lower_purple = np.array([125, 43, 46])
    upper_purple = np.array([155, 255, 255])
    color_list = []
    color_list.append(lower_purple)
    color_list.append(upper_purple)
    dict['purple'] = color_list

    return dict


def get_color(frame):
    print('go in get_color')
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = getColorList()
    for d in color_dict:
        mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
        # cv2.imwrite(d + '.jpg', mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary, None, iterations=2)
        img, cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in cnts:
            sum += cv2.contourArea(c)
        if sum > maxsum:
            maxsum = sum
            color = d

    return color

def getImage():
    os.system("adb shell /system/bin/screencap -p /sdcard/tmp/tupian.png")
    os.system("adb pull /sdcard/tmp/tupian.png /Users/steven/Desktop/lianliankan/tupian.png")
    img=cv2.imread('./tupian.png')
    # print(img.shape)
    cropImage=img[790:2207,45:1033]
    cv2.imwrite("./cropImage.png", cropImage)

    return cropImage

def getMatrix(cropImage):

    #对单个方块进行切割
    square_list=[]
    lenX=130
    blankX=13
    lenY=130
    blankY=13
    numX=7      #列数
    numY=10     #行数
    count=0
    types = []  # 记录颜色种类
    tmp=[]      #缓存队列
    imageMatrix=[]  #生成的矩阵

    for y in range(numY):
        for x in range(numX):
            square=cropImage[(lenY+blankY)*y:blankY*y+lenY*(y+1),(lenX+blankX)*x:blankX*x+lenX*(x+1)]
            cv2.imwrite("./tmp/{0}.png".format(count), square)
            square_list.append(square)
            count=count+1

    #获取方块主体颜色种类并生成矩阵

    count=0
    for square in square_list:
        print("tag:{0}".format(count))
        count = count + 1
        image_value = get_color(square)
        tmp.append(image_value)
        print(image_value)

        if len(tmp) == numX:
            imageMatrix.append(tmp)
            tmp=[]

        if image_value not in types:
            types.append(image_value)
    print("types:{0}".format(len(types)))

    return imageMatrix


def removeSquare(imageMatrix):
    for i in range(35):
        autoRemove(imageMatrix)

def autoRemove(imageMatrix):
    game_x=45
    game_y=790
    touchSize=65
    TIME_INTERVAL=0.5
    for i in range(0,len(imageMatrix)):
        for j in range(0,len(imageMatrix[0])):
            # 以上两个for循环，定位第一个选中点
            if imageMatrix[i][j] != 0:
                for m in range(0,len(imageMatrix)):
                    for n in range(0,len(imageMatrix[0])):
                        if imageMatrix[m][n] != 0:
                            # 后两个for循环定位第二个选中点
                            # 执行消除算法并返回
                            if canConnect(i,j,m,n,imageMatrix):

                                imageMatrix[i][j] = 0
                                imageMatrix[m][n] = 0
                                print('可消除点：'+ str(i+1) + ',' + str(j+1) + '和' + str(m+1) + ',' + str(n+1))

                                x1 = game_x + j*130+touchSize
                                y1 = game_y + i*130+touchSize
                                x2 = game_x + n*130+touchSize
                                y2 = game_y + m*130+touchSize

                                print("点击：({0},{1}),({2},{3})".format(x1,y1,x2,y2))
                                adbControl(x1,y1)
                                time.sleep(TIME_INTERVAL)

                                adbControl(x2,y2)
                                time.sleep(TIME_INTERVAL)
                                # win32api.SetCursorPos((x1 + 15,y1 + 18))
                                # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x1+15, y1+18, 0, 0)
                                # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x1+15, y1+18, 0, 0)
                                # time.sleep(TIME_INTERVAL)
                                #
                                # win32api.SetCursorPos((x2 + 15, y2 + 18))
                                # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x2 + 15, y2 + 18, 0, 0)
                                # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x2 + 15, y2 + 18, 0, 0)
                                # time.sleep(TIME_INTERVAL)
                                return True
    return False
    pass

def adbControl(x,y):
    os.system("adb shell input tap {0} {1}".format(x,y))

if __name__ == '__main__':
    cropImage=getImage()
    imageMatrix=getMatrix(cropImage)
    removeSquare(imageMatrix)
    # print(imageMatrix)


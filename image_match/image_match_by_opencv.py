#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PIL import ImageGrab
import cv2 as cv
class ImageMatchByOpenCV:

    def find_image(self, target):
        base_path = os.path.join(os.getcwd(), 'source')

        # 构造大图图片的保存路径
        screen_path = os.path.join(base_path, 'screen.png')
        # 截取当前屏幕并保存成文件

        ImageGrab.grab().save(screen_path)
        # 分别获取大图和小图的图像对象
        screen = cv.imread(screen_path)
        template = cv.imread(os.path.join(base_path, target))
        # 进行模板匹配操作
        result = cv.matchTemplate(screen, template, cv.TM_CCOEFF_NORMED)
        min, max, min_loc, max_loc = cv.minMaxLoc(result)
        # max_loc是当模版图片在大图上匹配度最高时，模版图片的左上顶点对应的大图坐标


        similarity = max
        if similarity < 0.95:
            return -1, -1
        # 匹配度大于等于0.95的话我们认为是匹配的，接下来就计算中心点坐标
        # 模板对象可以通过shape属性来获取其宽高数据，但是大家要注意这个属性返回结果是一个元组，
        # 它的第一个元素表示的是高，第二个元素表示的才是宽。所以大家要注意取值的索引下标不要用错。
        x = int(max_loc[0]) + int(template.shape[1] / 2)
        y = int(max_loc[1]) + int(template.shape[0] / 2)

        return x, y

    def check_exist(self, target):
        x, y = self.find_image(target)
        return x != -1 and y != -1

if __name__ == '__main__':
    ImageMatchByOpenCV().find_image("set.png")
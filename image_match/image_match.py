#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageGrab
import os
import time


class ImageMatch:

    def __init__(self):
        # 定义大图和小图的图像对象
        self.screen = None
        self.template = None
        # 定义大图和小图的像素数据对象
        self.screen_data = None
        self.template_data = None

    # 定义一个像素比对的方法
    def compare(self, p1, p2):
        return p1[0] == p2[0] and p1[1] == p2[1] and p1[2] == p2[2] and p1[3] == p2[3]

    # 定义一个图像匹配的方法
    def find_image(self, target):
        base_path = os.path.join(os.getcwd(), 'source')
        # 分别获取大图和小图的图像对象
        self.screen = ImageGrab.grab().convert('RGBA')
        self.template = Image.open(os.path.join(base_path, target)).convert('RGBA')
        # 分别获取大图和小图的宽高数据
        screen_width, screen_height = self.screen.size
        template_width, template_height = self.template.size
        # 分别获取大图和小图的像素数据对象
        self.screen_data = self.screen.load()
        self.template_data = self.template.load()
        # 利用双层for循环来实现滑动比对的处理，其中外层for循环代表Y轴的滑动，内层for循环代表X轴的滑动
        for y in range(screen_height - template_height):
            for x in range(screen_width - template_width):
                # 利用条件分支来去完成比对，首先先进行5个特征点的比对，比对的结果均为真，我们就去进行全像素比对；
                # 否则就什么也不做，让它继续循环。
                if self.compare(self.screen_data[x, y], self.template_data[0, 0]) and\
                    self.compare(self.screen_data[x + template_width - 1, y],
                                 self.template_data[template_width - 1, 0]) and\
                    self.compare(self.screen_data[x, y + template_height - 1],
                                 self.template_data[0, template_height - 1]) and\
                    self.compare(self.screen_data[x + template_width - 1, y + template_height - 1],
                                 self.template_data[template_width - 1, template_height - 1]) and\
                    self.compare(self.screen_data[x + int(template_width / 2), y + int(template_height / 2)],
                                 self.template_data[int(template_width / 2), int(template_height / 2)]):
                    # 5个特征点已经比对成功，继续进行全像素匹配
                    is_match = self.check_match(x, y)
                    if is_match:
                        # 全像素匹配成功，我们就计算中心点坐标并返回
                        return x + int(template_width / 2),  y + int(template_height / 2)
        # 如果循环正常走完，意味着此时没有找到模板图片
        return -1, -1

    # 定义一个全像素匹配的方法
    def check_match(self, x, y):
        template_width, template_height = self.template.size
        # 利用双层for循环来完成像素点的滑动比对
        for small_y in range(template_height):
            for small_x in range(template_width):
                # 在这里检查不匹配的像素点，只要遇到一个不匹配的点，那么就返回False，代表全像素匹配失败。
                if not self.compare(self.screen_data[x + small_x, y + small_y], self.template_data[small_x, small_y]):
                    return False
        # 如果正常走完循环，代表匹配成功。
        return True

    # 定义一个检查指定模板是否存在的方法，用于断言
    def check_exist(self, target):
        x, y = self.find_image(target)
        return x != -1 and y != -1

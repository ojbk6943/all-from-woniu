#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pymouse import PyMouse
from pykeyboard import PyKeyboard
import os
import time

# from training.phase21.CBT.image_match.image_match import ImageMatch
from image_match_by_opencv import ImageMatchByOpenCV


def delay(func):
    def wrapper(*args, **kwargs):

        func(*args, **kwargs)
        time.sleep(1)
        print('delay 1s.')
    return wrapper


class ImageTest:

    def __init__(self):

        #生成鼠标实例
        self.mouse = PyMouse()

        #生成键盘实例
        self.keyboard = PyKeyboard()

        #实例化模版匹配的类
        self.match = ImageMatchByOpenCV()

    def start_app(self, cmd):
        os.system('start /b %s' % cmd)
        time.sleep(6)

    @delay
    def click(self, target):
        x, y = self.match.find_image(target)
        if x == -1 or y == -1:
            print('not found %s.' % target)
            return
        self.mouse.click(x, y)
        print('click %s at [%d, %d].' % (target, x, y))

    def double_click(self, target):
        x, y = self.match.find_image(target)
        if x == -1 or y == -1:
            print('not found %s.' % target)
            return
        self.mouse.click(x, y, n=2)
        print('double click %s at [%d, %d].' % (target, x, y))
        time.sleep(1)

    def input_text(self, target, content):
        self.double_click(target)
        self.keyboard.type_string(content)
        print('input %s at %s.' % (content, target))
        time.sleep(1)

    def select(self, target, count=1):
        self.click(target)
        for i in range(count):
            self.keyboard.press_key(self.keyboard.down_key)
            time.sleep(1)
        self.keyboard.press_key(self.keyboard.enter_key)
        print('select No.%d at %s.' % (count + 1, target))
        time.sleep(1)

    def start_test(self):
        self.start_app('java -jar JavaSwingCalc.jar')
        self.input_text('numberx.png', '200')
        self.input_text('numbery.png', '100')
        self.select('calctype.png')
        self.click('docalc.png')
        if self.match.check_exist('result.png'):
            print('test success.')
        else:
            print('test fail.')
        self.click('doclose.png')



if __name__ == '__main__':
    ImageTest().start_test()




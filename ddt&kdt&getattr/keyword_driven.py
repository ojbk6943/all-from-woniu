#! /usr/bin/env python
# -*- coding: utf-8 -*-

import csv


class KDT:

    def keyword_test(self):
        module = __import__('training.phase21.CBT.Reflection.agileone', fromlist=['agileone'])
        classes = dir(module)
        for class_name in classes:
            if not class_name.startswith('_'):
                class_obj = getattr(module, class_name)()
                with open('./data/keyword.txt', 'r') as f:
                    reader = csv.reader(f)
                    for keywords in reader:
                        method_name = keywords.pop(0).lower().replace(' ', '_')
                        if hasattr(class_obj, method_name):
                            getattr(class_obj, method_name)(*keywords)

    def keyword_chinese_test(self):
        module = __import__('training.phase21.CBT.Reflection.agileone', fromlist=['agileone'])
        classes = dir(module)
        for class_name in classes:
            if not class_name.startswith('_'):
                class_obj = getattr(module, class_name)()
                with open('./data/keyword_chinese.txt', 'r', encoding='utf8') as f:
                    reader = csv.reader(f)
                    dictionary = {'打开浏览器': 'open_browser', '输入账号': 'input_text', '输入密码': 'input_password',
                                  '登录': 'click_button', '等待': 'wait', '关闭浏览器': 'close_browser'}
                    for keywords in reader:
                        method_name = dictionary[keywords.pop(0)]
                        if hasattr(class_obj, method_name):
                            getattr(class_obj, method_name)(*keywords)


if __name__ == '__main__':
    KDT().keyword_chinese_test()

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import random


class Student:

    def __init__(self):
        self._name = None
        self._age = None
        self._sex = None

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_age(self):
        return self._age

    def set_age(self, age):
        self._age = age

    def get_sex(self):
        return self._sex

    def set_sex(self, sex):
        self._sex = sex

    def get_student(self):
        return self._name, self._age, self._sex

    def set_student(self, name, age, sex):
        self._name = name
        self._age = age
        self._sex = sex


if __name__ == '__main__':
    stu1 = Student()
    stu1._name = '张三'
    print(stu1._name)
    stu1.set_age(19)
    print(stu1.get_age())
    print('**********************************')
    module = __import__('training.phase21.CBT.Reflection.student', fromlist=['student'])
    class_name = getattr(module, 'Student')
    stu2 = class_name()
    # 第二种获取类的对象的方法
    stu3 = module.Student()
    # 检查指定对象中是否有传入的属性
    if hasattr(stu1, '_name'):
        # 获取指定对象的指定属性的值
        print(getattr(stu1, '_name'))
    if hasattr(stu1, 'get_name'):
        # 获取指定对象的指定函数 无参数 的第一种方法
        method = getattr(stu1, 'get_name')
        print(method())
        # 第二种方法
        print(getattr(stu1, 'get_name')())
    if hasattr(stu2, 'set_name'):
        # 获取指定对象的指定函数 有参数 的第一种方法
        method = getattr(stu2, 'set_name')
        method('李四')
        print(getattr(stu2, 'get_name')())
        # 第二种方法
        getattr(stu2, 'set_age')(25)
        print(getattr(stu2, 'get_age')())
    if hasattr(stu1, '_age'):
        print(getattr(stu1, '_age'))
        # 删除属性的方法
        delattr(stu1, '_age')
        # print(getattr(stu1, '_age'))
    print('************************************')
    # 获取指定类的对象的全部属性和方法名列表
    # methods = stu3.__dir__()
    methods = dir(stu3)
    methods.sort(reverse=True)
    for method_name in methods:
        if not method_name.startswith('_'):
            method = getattr(stu3, method_name)
            # 获取指定方法的参数个数
            count = method.__code__.co_argcount - 1
            args = []
            for i in range(count):
                args.append(random.randint(100, 999))
            if method_name.startswith('get'):
                print(method_name, method(*args))
            else:
                method(*args)
                print(method_name, args)

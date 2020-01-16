#! /usr/bin/env python
# -*- coding: utf-8 -*-

from training.phase21.CBT.Reflection.calculator import Calculator as cal


class CalculatorTest:

    def test_add(self):
        result = cal.add(3, 5)
        if result == 8:
            print('test success.')
        else:
            print('test fail.')

    def test_sub(self):
        result = cal.sub(9, 3)
        if result == 6:
            print('test success.')
        else:
            print('test fail.')


if __name__ == '__main__':
    test = CalculatorTest()
    methods = dir(test)
    for method_name in methods:
        if method_name.startswith('test'):
            getattr(test, method_name)()

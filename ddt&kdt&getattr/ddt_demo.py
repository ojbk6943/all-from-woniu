#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ddt import ddt, data, file_data, unpack
import csv
import os
import unittest
from training.phase21.CBT.Reflection.calculator import Calculator as cal


def csv_reader(file):
    if not os.path.exists(file):
        return None
    with open(file, 'r') as f:
        reader = csv.reader(f)
        content = []
        for line in reader:
            line_data = []
            for el in line:
                line_data.append(cal.aton(el))
            content.append(line_data)
        return content


@ddt
class CalculatorTestCase(unittest.TestCase):

    @data([8, 3, 5], [18, 9, 1], [12, 7, 5])
    @unpack
    def test_add(self, expected, num1, num2):
        self.assertEqual(expected, cal.add(num1, num2))

    @data(*csv_reader('./data/sub_data.csv'))
    @unpack
    def test_sub(self, expected, num1, num2):
        self.assertEqual(expected, cal.sub(num1, num2))

    @file_data('./data/multi_data.json')
    @unpack
    def test_multi(self, expected, num1, num2):
        self.assertEqual(expected, cal.multi(num1, num2))

    @file_data('./data/div_data.yaml')
    @unpack
    def test_div(self, expected, num1, num2):
        self.assertEqual(expected, cal.div(num1, num2))


if __name__ == '__main__':
    unittest.main(verbosity=2)

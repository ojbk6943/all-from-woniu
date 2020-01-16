#! /usr/bin/env python
# -*- coding: utf-8 -*-


class Calculator:

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def sub(a, b):
        return a - b

    @staticmethod
    def multi(a, b):
        return a * b

    @staticmethod
    def div(a, b):
        return a / b

    @staticmethod
    def aton(num):
        if not isinstance(num, str):
            return num
        try:
            return int(num)
        except ValueError:
            return float(num)
        except Exception:
            return num

#! /usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import os
import time
import random

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Common:

    driver = None

    # 这是单例模式的一种实现
    @classmethod
    def get_driver(cls, browser_type='firefox'):
        if cls.driver is None:
            if browser_type == 'firefox' or browser_type == 'ff':
                driver_path = os.path.join(os.getcwd(), 'driver/geckodriver.exe')
                cls.driver = webdriver.Firefox(executable_path=driver_path)
            elif browser_type == 'chrome' or browser_type == 'gc':
                driver_path = os.path.join(os.getcwd(), 'driver/chromedriver.exe')
                cls.driver = webdriver.Chrome(executable_path=driver_path)
            else:
                driver_path = os.path.join(os.getcwd(), 'driver/IEDriverServer.exe')
                cls.driver = webdriver.Ie(executable_path=driver_path)
        cls.driver.set_page_load_timeout(5)
        cls.driver.implicitly_wait(5)
        return cls.driver

    # 定义一个检查元素是否存在的方法
    @classmethod
    def element_is_presence(cls, by, value):
        try:
            cls.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False

    # 定义一个元素的显示等待方法
    @classmethod
    def wait_element_of_presence(cls, by, value, timeout=3):
        # 第一种方法
        # for i in range(timeout):
        #     try:
        #         cls.driver.find_element(by, value)
        #         return True
        #     except NoSuchElementException:
        #         time.sleep(1)
        # return False
        # 第二种方法
        # try:
        #     WebDriverWait(cls.driver, timeout).until(expected_conditions.presence_of_element_located((by, value)))
        #     return True
        # except TimeoutException:
        #     return False
        # 第三种方法
        try:
            WebDriverWait(cls.driver, timeout).until(lambda dr: dr.find_element(by, value))
            return True
        except TimeoutException:
            return False

    # 普通方法、静态方法和类方法之间的区别
    # 1. 普通方法使用的时候，必须通过其所在类的实例化对象来调用，而类方法或静态方法不需要，它们只用类名的方式就可以调用了，无需实例化类。
    # 2. 静态方法没有默认的参数，而普通方法默认首个参数为self，类方法默认首个参数为cls。
    # 3. 静态方法多用于方法体中没有和其所属类相关东西调用的场景，类方法多用于方法体中有调用其所属类的属性或方法的场景。
    @staticmethod
    def random_sleep():
        time.sleep(random.randint(2, 10))

    @classmethod
    def close_browser(cls):
        cls.driver.quit()
        cls.driver = None

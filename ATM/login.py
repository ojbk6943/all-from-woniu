#! /usr/bin/env python
# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

from Reporter import Reporter
from common import Common



class Login:

    def __init__(self):
        self.driver = Common.get_driver()
        self.module = '登录'
        self.report = Reporter('1.0.1')

    def prepare(self):
        self.driver.get('http://jacky-pc/agileone/')
        if Common.element_is_presence(By.ID, 'username') and 'AgileOne' in self.driver.title:
            print('open homepage success.')
        else:
            print('open homepage fail.')

    def finish(self):
        Common.close_browser()
        self.report.generate_html()

    def main_test(self):
        self.prepare()
        self.test_login()
        self.finish()

    def do_login(self, name, password):
        user = self.driver.find_element_by_id('usernam')
        user.clear()
        user.send_keys(name)
        psw = self.driver.find_element_by_id('password')
        psw.clear()
        psw.send_keys(password)
        self.driver.find_element_by_id('login').click()

    def test_login(self):
        username = 'admin'
        password = 'admin1'
        try:
            self.do_login(username, password)
            if Common.wait_element_of_presence(By.ID, 'welcome') and username in self.driver.find_element_by_id(
                    'welcome').text:
                self.report.write_report(self.module, 'UI测试', 'AG-001', '正确的账户信息登录测试', '成功', '无', '无')
            else:
                self.report.write_report(self.module, 'UI测试', 'AG-001', '错误的账户信息登录测试', '失败', '断言错误', '无')
        except Exception as e:
            screenshot = self.report.capture_screen(self.driver)
            self.report.write_report(self.module, 'UI测试', 'AG-001', '错误的账户信息登录测试', '错误', str(e), screenshot)

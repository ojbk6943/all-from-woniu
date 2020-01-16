#! /usr/bin/env python
# -*- coding: utf-8 -*-


class Agileone:

    def open_browser(self, url):
        print('open homepage %s.' % url)

    def input_text(self, locator, content):
        print('input %s at %s.' % (content, locator))

    def input_password(self, locator, password):
        self.input_text(locator, password)

    def click_button(self, locator):
        print('on click at %s.' % locator)

    def wait(self, timeout):
        print('wait %ss.' % timeout)

    def close_browser(self):
        print('close browser.')

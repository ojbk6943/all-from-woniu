#! /usr/bin/env python
# -*- coding: utf-8 -*-
from login import Login


# Login().main_test()
login = Login()
login.prepare()
login.test_login()
login.finish()
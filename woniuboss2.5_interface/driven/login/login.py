import unittest
import HTMLTestRunner
from testcase.TestLogin.TestLogin import TestLogin


def login():
    suite=unittest.TestSuite()
    loder=unittest.TestLoader()
    test=loder.loadTestsFromTestCase(TestLogin)
    with open("../../report/report04.html","w",encoding="utf8") as file:
        run=HTMLTestRunner.HTMLTestRunner(stream=file,verbosity=2,title=None,description=None)
        run.run(test)



login()
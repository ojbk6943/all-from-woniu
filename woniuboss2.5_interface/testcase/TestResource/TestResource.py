from nose_parameterized import parameterized
import unittest
import requests

from util.Utility import Utility
data=Utility.read_json("../../testdata/Resource/ResourceData")
cookie=Utility.read_json("../../config/login_cooike")
url_data=Utility.read_json("../../config/base_config")
url=url_data["protocol"]+url_data["host"]+url_data["port"]+url_data["program"]

session=requests.session()
session.post(url,cookie)

class TestResource(unittest.TestCase):

    @parameterized.expand(data)
    def test_resource(self,param,expect):
        resp=session.post(url,param)
        if resp.status_code==200:
            actual="pass"
        else:
            actual="fail"
        self.assertEqual(actual,expect)

if __name__ == '__main__':
    unittest.main()







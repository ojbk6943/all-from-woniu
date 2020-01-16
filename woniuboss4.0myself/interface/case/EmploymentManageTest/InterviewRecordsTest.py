

import requests

import unittest

from parameterized import parameterized

from interface.util.Utility import Utility

record_query_data=Utility.read_json("../../test_data/EmploymentManageData/record_query_data")

decode_data=Utility.read_json("../../test_data/EmploymentManageData/decode_data")

class RecordQuery(unittest.TestCase):

    def setUp(self):
        login_data=Utility.read_json("../../config/data_cookie")["login_data"]
        login_url=Utility.read_json("../../config/data_cookie")["login_url"]
        self.session=requests.session()
        self.session.post(login_url,login_data)

        base_url_data = Utility.read_json("../../config/data_base")
        self.base_url = base_url_data["protocol"] + base_url_data["host"] + base_url_data["port"] + \
                   base_url_data["program"]
    @parameterized.expand(decode_data)
    def test_decode(self,url,data,expect):
        resp=self.session.post(self.base_url+url,data)

        if resp.text=="yes":
            actual="pass"
        else:
            actual="fail"
        self.assertEqual(expect,actual)
    @parameterized.expand(record_query_data)
    def test_records_query(self,url,data,expect):
        resp=self.session.post(self.base_url+url,data)
        if resp.json()["totalRow"] != 0:
            actual="pass"
        else:
            actual="fail"
        self.assertEqual(expect,actual)
if __name__ == '__main__':
    unittest.main()

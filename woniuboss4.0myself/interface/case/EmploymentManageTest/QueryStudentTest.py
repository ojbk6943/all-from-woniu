
import requests
import unittest

from parameterized import parameterized

from interface.util.Utility import Utility

query_student_data=Utility.read_json("../../test_data/EmploymentManageData/query_student_data")
interview_data=Utility.read_json("../../test_data/EmploymentManageData/interview_data")
decode_data=Utility.read_json("../../test_data/EmploymentManageData/decode_data")
class QueryStudent(unittest.TestCase):

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

    @parameterized.expand(query_student_data)
    def test_query_student(self,url,data,expect):
        resp=self.session.post(self.base_url+url,data)

        if len(resp.text) != 0 :
            actual="pass"
        else:
            actual="fail"
        self.assertEqual(expect,actual)

    @parameterized.expand(interview_data)
    def test_interview(self,url1,data1,url2,url3,url4,data4,expect):

        resp1=self.session.post(self.base_url+url1,data1)
        resp2=self.session.post(self.base_url+url2,data1)
        resp3=self.session.get(self.base_url+url3)
        resp4=self.session.post(self.base_url+url1,data1)
        resp5=self.session.post(self.base_url+url4,data4)
        resp6=self.session.post(self.base_url+url1,data1)
        resp7=self.session.post(self.base_url+url2,data1)

        if resp7.json()["list"][0]["intent_salary"]=="80000":
                actual="pass"
        else:
            actual="fail"

        self.assertEqual(actual,expect)

if __name__ == '__main__':
    unittest.main()
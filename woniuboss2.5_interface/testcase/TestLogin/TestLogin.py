from common.login.login import Login
import unittest
import requests

from util.Service import Service
from util.Utility import Utility

session=requests.session()

data=Utility.read_json("../../config/login_cooike")
url_data=Utility.read_json("../../config/base_config")
url=url_data["protocol"]+url_data["host"]+url_data["port"]+url_data["program"]
class TestLogin(unittest.TestCase):

    def setUp(self):
        self.session=requests.session()

    def test_login(self):
        Login.open_homepage(self.session,url)
        Login.login(self.session,url,data)

if __name__ == '__main__':
    unittest.main()
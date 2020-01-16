



class Login():

    @classmethod
    def open_homepage(cls,session,url):
        resp_homepage=session.get(url)
        if "Boss系统" in resp_homepage.text:
            print("打开首页成功")
            return resp_homepage

    @classmethod
    def login(cls,session,url,data):
        resp_login=session.post(url,data)
        if resp_login.status_code==200:
            print("登录成功")
            return resp_login

if __name__ == '__main__':
    Login.open_homepage()
    Login.login()



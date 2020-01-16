#! /usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pymysql
import os
import time
import zipfile


# 代码思路
# 首先安装pymysql模块
class Reporter:

    def __init__(self, version):
        self.version = version

    # 定义一个测试报告数据的方法
    # 1. 利用pymysql模块的connect方法来构造一个数据库连接对象conn
    # 2. 通过conn对象来获取游标对象cursor
    # 3. 拼接sql的插入指令 insert into report(fields) values(values);
    # 4. 利用游标对象cursor的execute方法来执行上面的sql
    # 5. 执行完以后注意要commit一下，否则数据库内容不会改变。
    # 6. 最后清理资源
    def write_report(self, module, testtype, caseid, casetitle, result, error, screenshot):
        conn = pymysql.connect(user='root', passwd='root',
                               host='jacky-pc', db='woniucbt', charset='utf8')
        cursor = conn.cursor()
        testtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        sql = "insert into report(version, module, testtype, caseid, casetitle, result, testtime, error, screenshot)" \
              " values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"\
              % (self.version, module, testtype, caseid, casetitle, result, testtime, error, screenshot)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def get_time(self):
        now = time.localtime(time.time())
        current_date = time.strftime("%Y%m%d", now)
        current_time = time.strftime("%Y%m%d_%H%M%S", now)
        return current_date, current_time

    def get_report_folder(self, c_date=None):
        if c_date is None:
            c_date = ''
        report_folder = os.path.abspath('.') + '\\report\\report%s_%s' % (c_date, self.version)
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
        return report_folder

    # 定义一个截取屏幕的方法
    def capture_screen(self, driver):
        c_date, c_time = self.get_time()
        report_folder = self.get_report_folder(c_date)
        screenshot_folder = os.path.join(report_folder, 'screenshot')
        # 检查截屏文件夹是否存在，不存在就创建
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        # 构造截屏保存的路径
        screenshot = os.path.join(screenshot_folder, c_time + '.png')
        # 截取当前屏幕
        driver.get_screenshot_as_file(screenshot)
        # 返回的实际上是截屏文件的相对路径，因为/在向数据库保存时均会报错，所以用-代替/，将来用的时候换回来即可。
        return "screenshot-" + c_time + ".png"

    # 定义一个自动生成html测试报告的方法
    # 1. 利用pymysql模块的connect方法来构造一个数据库连接对象conn
    # 2. 通过conn对象来获取游标对象cursor
    # 3. 拼接sql的查询指令 select * from report where version = self.version;
    # 4. 利用cursor对象的execute方法来执行sql
    # 5. 利用cursor对象的fetchall方法来获取结果集result，结果集是一个元组类型。
    # 6. 首先对result的长度进行检查，如果其长度不大于0，那么就输出当前版本没有测试结果的信息，并且返回退出方法。
    # 7. 如果长度大于0，那么我们就要利用文件处理的open方法读取template.html文件到content变量中。
    # 8. 首先替换content变量中的$test-version为真实版本。
    # 9. 接下来构造sql指令去查询获取成功、失败、错误的个数
    # 10. 成功 select count(*) from where version = self.version and result = '成功';
    # 11. 利用cursor对象的fetchone方法来获取结果集
    # 12. 失败 select count(*) from where version = self.version and result = '失败';
    # 13. 错误 select count(*) from where version = self.version and result = '错误';
    # 14. 依照成功的处理分别去获取失败与错误的结果，并针对content去进行替换即可。
    # 15. 继续构造查询最后一条记录的时间的sql，select testtime from report where version = self.version order by id desc limit 0, 1;
    # 16. 最后利用fetchone来获取时间数据并替换content变量中的$test-date和$last-time
    # 17. 定义一个变量test_result用于保存每一行的数据
    # 18. 利用循环每次取result的一行数据来去拼接html的行记录代码并将其保存到test_result中
    # 19. 在拼接html代码时注意测试结果和截图栏位数据需要做一些简单的检查，根据值去使用不同的html代码
    # 20. 当循环走完我们就去利用test_result去替换content变量中的$test-result值
    # 21. 利用文件处理的open方法去写入content到指定的html报告文件中
    # 22. 最后去清理资源即可。
    def generate_html(self):
        conn = pymysql.connect(user='root', passwd='root', host='jacky-pc', db='woniucbt', charset='utf8')
        cursor = conn.cursor()
        sql = "select * from report where version = '%s'" % self.version
        cursor.execute(sql)
        results = cursor.fetchall()
        if not len(results):
            return
        tempate_path = os.path.abspath('.') + '\\report\\template.html'
        tempate = open(tempate_path, mode='r', encoding='UTF-8')
        content = tempate.read()
        version = results[0][1]
        content = content.replace("$test-version", version)
        sql_base = "select count(*) from report where version='%s' and " % version
        sql_pass = sql_base + "result='成功'"
        cursor.execute(sql_pass)
        pass_count = cursor.fetchone()[0]
        content = content.replace("$pass-count", str(pass_count))
        sql_fail = sql_base + "result='失败'"
        cursor.execute(sql_fail)
        fail_count = cursor.fetchone()[0]
        content = content.replace("$fail-count", str(fail_count))
        sql_error = sql_base + "result='错误'"
        cursor.execute(sql_error)
        error_count = cursor.fetchone()[0]
        content = content.replace("$error-count", str(error_count))
        sql_last = "select testtime from report where version='%s' order by id desc limit 0,1" % version
        cursor.execute(sql_last)
        last_time = cursor.fetchone()[0]
        content = content.replace("$last-time", str(last_time))
        content = content.replace("$test-date", str(last_time))
        test_result = ""
        for record in results:
            test_result += "<tr height='40'>"
            test_result += "<td width='7%'>" + str(record[0]) + "</td>"
            test_result += "<td width='9%'>" + record[2] + "</a></td>"
            test_result += "<td width='9%'>" + record[3] + "</td>"
            test_result += "<td width='7%'>" + record[4] + "</td>"
            test_result += "<td width='20%'>" + record[5] + "</td>"
            if record[6] == '成功':
                test_result += "<td width='7%' bgcolor='lightgreen'>" + record[6] + "</td>"
            elif record[6] == '失败':
                test_result += "<td width='7%' bgcolor='red'>" + record[6] + "</td>"
            elif record[6] == '错误':
                test_result += "<td width='7%' bgcolor='yellow'>" + record[6] + "</td>"
            test_result += "<td width='16%'>" + str(record[7]) + "</td>"
            test_result += "<td width='15%'>" + record[8] + "</td>"
            screenshot = record[9].replace('-', '/')
            if screenshot == '无':
                test_result += "<td width='10%'>" + screenshot + "</td>"
            else:
                test_result += "<td width='10%'><a href='" + screenshot + "'>查看截图</a></td>"
            test_result += "</tr>\r\n"
        content = content.replace("$test-result", test_result)
        c_date, c_time = self.get_time()
        report_folder = self.get_report_folder(c_date)
        report_path = os.path.join(report_folder, c_time + '_cbt.html')
        report = open(report_path, mode='w', encoding='utf8')
        report.write(content)
        tempate.close()
        report.close()
        cursor.close()
        conn.close()

    # 定义一个压缩文件的方法
    def compress_report(self):
        filelist = []
        c_date, c_time = self.get_time()
        report_folder = self.get_report_folder(c_date)
        print('report_folder:', report_folder)
        root_folder = os.path.split(report_folder)[1]
        print('root_folder:', root_folder)
        zipfilename = 'report\\report_' + c_time + '.zip'
        # 构造一个压缩文件对象
        zip = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_LZMA)
        # 进行文件的遍历操作
        for root, folders, filenames in os.walk(report_folder):
            for folder in folders:
                filelist.append(os.path.join(root, folder))
            for filename in filenames:
                if 'Thumbs.db' not in filename:
                    filelist.append(os.path.join(root, filename))
        for file in filelist:
            # print('file：', file)
            # print(file.split(root_folder))
            # zip的write方法第一个参数用于指定文件路径，而第二个参数用于指定锚位置
            zip.write(file, file.split(root_folder)[1])
            # zip.write(file)
        zip.close()
        return zipfilename

    # 定义一个发送邮件的方法
    def send_mail(self, attachment):
        # 定义邮件的发件人
        sender = 'student@woniuxy.com'
        # 定义邮件的收件人列表
        receivers = ['wangbin@woniuxy.com', 'test@qq.com']
        # 简单的邮件内容定义
        # message = MIMEText('邮件内容', 'text', 'utf-8')
        # message['Subject'] = Header('邮件标题', 'utf-8')
        # 包含附件的邮件内容定义
        message = MIMEMultipart()
        message.attach(MIMEText('<p style="color: red; font-size: 30px">'
                           '这是一封来自Python发送的测试邮件的内容...</p>',
                           'html', 'utf-8'))
        message['Subject'] = Header('一封Python发送的邮件', 'utf-8')
        att = MIMEApplication(open(attachment, 'rb').read())
        att.add_header('Content-Disposition', 'attachment', filename=os.path.split(attachment)[1])
        message.attach(att)
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect('mail.woniuxy.com', 25)
            smtpObj.login(user='student@woniuxy.com', password='stu123')
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")


if __name__ == '__main__':
    report = Reporter('1.0.1')
    # report.write_report('登录功能', '接口测试', 'TC-001',
    #                     'Agileone的正常登录测试', '成功', '无', '无')
    # report.write_report('登录功能', '接口测试', 'TC-002',
    #                     'Agileone的错误登录测试', '失败', '断言失败', 'screenshot-20190415_123540.png')
    # report.write_report('需求提案', 'GUI测试', 'TC-002',
    #                     'Agileone的错误登录测试', '错误', '无法连接到服务器', 'screenshot-20190415_123845.png')
    # report.generate_html()
    comp_file = report.compress_report()
    print(comp_file)

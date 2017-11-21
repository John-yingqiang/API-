# -*- coding: utf-8 -*-
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header
import zipfile
import os
reload(sys)
sys.setdefaultencoding('utf8')

def sendEmail(subject = "测试报告", path_to_html =""):
    _user = "qiang.ying@sofmit.com"
    smtp_server = "mail.sofmit.com"
    _to = [""]
    user_name = ""
    psword = ""

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"]    = _user
    msg["To"]      = ",".join(_to)

    part = MIMEText("这是自动化测试邮件，自动发送")
    msg.attach(part)

    # part = MIMEApplication(open('C:/Users/Administrator/Desktop/background.bmp','rb').read())
    # part.add_header('Content-Disposition', 'attachment', filename="background.bmp")
    # msg.attach(part)

    part = MIMEApplication(open(path_to_html + '/Report/report_file.zip','rb').read())
    part.add_header('Content-Disposition', 'attachment', filename="report_file.zip")
    msg.attach(part)
    #
    # part = MIMEApplication(open(path_to_html + '/log/test_log.txt','rb').read())
    # part.add_header('Content-Disposition', 'attachment', filename="test_log.txt")
    # msg.attach(part)

    smtp = smtplib.SMTP("mail.sofmit.com", timeout=30)
    smtp.login(_user, psword)
    smtp.sendmail(_user, _to, msg.as_string())
    smtp.close()

def zip_file(file_dir, zip_file_name="report_file.zip"):
    z =zipfile.ZipFile(zip_file_name, 'w')
    if os.path.isdir(file_dir):
        for file in os.listdir(file_dir):
            if file != zip_file_name:
                file_path = file_dir + "/" + file
                z.write(file_path, file)
        z.close()

if __name__ == "__main__":
    if len(os.sys.argv) != 2:
        print u"请输入需要压缩的文件夹路径"
        exit(-1)
    else:
        print "dir_path:{}".format(sys.argv[-1] + "/Report")
        zip_file(sys.argv[-1] + "/Report")
    sendEmail(path_to_html = os.sys.argv[-1])


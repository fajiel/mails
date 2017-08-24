#-*- coding:utf-8 -*-
import os
import yaml
from datetime import datetime
from database.models import User
from database.manage import Session
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

SENDER_FILE = os.path.join(os.path.dirname(__file__), 'config/sender.yaml')
MSG_FILE = os.path.join(os.path.dirname(__file__), 'config/mail.html')

class SendMSG():
    def __init__(self):
        self.session = Session()
        self.msg = ""
        self.to_list = []
        self.content = self.__read_html(MSG_FILE)
        self._get_sender()
        super(SendMSG, self).__init__()

    def get_mails(self):
        query = self.session.query(User.mail, User.uid)
        query_list = query.filter_by(white=1).all()
        self.to_list = [(query_obj.mail, query_obj.uid) for query_obj in query_list]

    def __read_yaml(self, file):
        f = open(file)
        result = yaml.load(f)
        return result

    def __format_addr(self, str):
        name, addr = parseaddr(str)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def _get_sender(self):
        cfg_dict = self.__read_yaml(SENDER_FILE)
        self.from_addr = cfg_dict.get("from", {}).get("addr", "")
        self.from_name = cfg_dict.get("from", {}).get("name", "")
        self.from_pwd = cfg_dict.get("from", {}).get("pwd", "")
        self.to_addr = cfg_dict.get("to", {}).get("addr", "")
        self.to_name = cfg_dict.get("to", {}).get("name", "")
        self.subject = cfg_dict.get("subject", "")
        self.smtp = cfg_dict.get("smtp", "")

    def __read_html(self, file):
        return open(file, "r", encoding="utf-8").read()

    def send_mail(self, server, mail_to, uid):
        self.msg = MIMEText(self.content.format('{}'.format(uid)), 'html', 'utf-8')
        self.msg['From'] = self.__format_addr(u'{}<{}>'.format(self.from_name, self.from_addr))#我方邮箱名称
        self.msg['To'] = self.__format_addr(u'{}<{}>'.format(self.to_name, self.to_addr))#对方邮箱名称
        self.msg['Subject'] = Header(self.subject, 'utf-8').encode()#主题
        issucc = True
        try:
            server.sendmail(self.from_addr, mail_to, self.msg.as_string())
        except:
            issucc = False
        return issucc

    def update_db(self, issucc, mail):
        query = self.session.query(User)
        query_obj = query.filter_by(mail=mail).first()
        if issucc:
            query_obj.status = 1
            query_obj.send_times += 1
            query_obj.last_time = str(datetime.now())
        else:
            query_obj.status = 0

        self.session.merge(query_obj)
        self.session.commit()

    def send_msg(self):
        server = smtplib.SMTP(self.smtp, 25)
        server.set_debuglevel(1)
        server.login(self.from_addr, self.from_pwd)
        for mail_to, uid in self.to_list:
            issucc = self.send_mail(server, mail_to, uid)
            self.update_db(issucc, mail=mail_to)

        server.quit()
        self.session.close()


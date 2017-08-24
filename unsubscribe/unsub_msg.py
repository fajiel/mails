#-*- coding:utf-8 -*-

from database.models import User
from database.manage import Session

class UnsubMSG():
    def __init__(self, uid):
        self.session = Session()
        self.uid = uid
        self.mail = uid
        super(UnsubMSG, self).__init__()

    def unsub_mail(self):
        query = self.session.query(User)
        query_obj = query.filter_by(uid=self.uid).first()
        if query_obj:
            self.mail = query_obj.mail
            query_obj.white = 0
            self.session.merge(query_obj)
            self.session.commit()
        self.session.close()

#-*- coding:utf-8 -*-
from database.models import User
from database.manage import Session
import uuid

user_list = [
    {
        "uid": uuid.uuid1().hex,
        "name": "name",
        "mail": "mail_name@163.com",
    },
]

class UploadUser():
    def __init__(self):
        super(UploadUser, self).__init__()
        self.session = Session()
        self.add_num = 0

    def upload_user(self, user_list):
        print(u"用户列表共有{}个邮箱！".format(len(user_list)))
        for user_dict in user_list:
            user_mail = user_dict.get("mail", "")
            query_obj = self.session.query(User).filter_by(mail=user_mail).first()
            if query_obj:
                continue
            self.add_num += 1
            print(u"{},为新增邮箱！".format(user_mail))
            self.session.add(User(**user_dict))
            self.session.commit()
        print(u"本次新增邮箱{}个！".format(self.add_num))
        self.session.close()


def main(user_list):
    uu = UploadUser()
    uu.upload_user(user_list)

if __name__ == "__main__":
    main(user_list)
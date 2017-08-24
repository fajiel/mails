# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, SMALLINT, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TIMESTAMP
from datetime import datetime

DB_SETTING = {
    'drivername': 'mysql+mysqlconnector',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'Mail',
    'username': 'root',
    'password': '',
    'query': {
        'charset': 'utf8'
    }
}

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    uid = Column(String(100))
    mail = Column(String(255), nullable=False, primary_key=True)
    name = Column(String(50))
    white = Column(SMALLINT, default=1, doc=u"若用户退订，则白名单置为0")
    status = Column(SMALLINT, default=1, doc=u"表示最后一次发送是否成功")
    send_times = Column(Integer, default=0, doc=u"向用户发送邮件总次数")
    add_time = Column(TIMESTAMP, nullable=False, default=str(datetime.now()))
    last_time = Column(TIMESTAMP)

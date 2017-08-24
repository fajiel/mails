from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://root:''@localhost:3306/Mail?charset=utf8', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
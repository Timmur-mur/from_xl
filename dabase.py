from sqlalchemy import create_engine, engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String

engine = create_engine('postgresql://postgres:pqpass@localhost/url_db')
session = Session(bind=engine)

Base = declarative_base()

class Urls(Base):
    __tablename__ = 'urls'
    
    #id = Column(Integer, autoincrement=True)
    url = Column(String, primary_key=True)
    comment = Column(String)


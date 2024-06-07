
from sqlalchemy import Column,Integer,String
from .database import Base

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username=Column(String,primary_key=True,index=True)
    email=Column(String,primary_key=True,index=True)
    password=Column(String,primary_key=True,index=True)



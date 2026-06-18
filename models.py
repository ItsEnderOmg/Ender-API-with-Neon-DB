#Here you create the colums to store information of the rows

#You need to import the Datatypes that you're going to use in the columns
from sqlalchemy import Column, Integer, String
from db_config import Base

class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
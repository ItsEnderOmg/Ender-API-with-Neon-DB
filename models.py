#Here you create the colums to store information of the rows

#You need to import the Datatypes that you're going to use in the columns
from sqlalchemy import Integer, String
# You'll use this ones to prevent typing errors with pydantic later (you dont need Colum from sqlalchemy anymore)
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
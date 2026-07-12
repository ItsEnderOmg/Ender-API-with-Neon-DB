from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Esto es pa cargar las variables secretas q creaste en .env
load_dotenv()
#Le asigna el valor de "DATABASE_URL"
DATABASE_URL = os.getenv("DATABASE_URL")

# Before creating the engine, you check if the value of the DATABASE_URL is None, if it's you raise an error
if DATABASE_URL is None:
    raise ValueError("Variable 'DATABASE_URL' is not defined, check the .env URL.")

# Pylance would raise an error here, because 'DATABASE_URL' could be None, but the previous 'raise' handles it (TYPE NARROWING)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
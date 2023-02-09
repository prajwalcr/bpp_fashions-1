import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@bpp_fashions-1-db-1:5432/bpp'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

Base = declarative_base()

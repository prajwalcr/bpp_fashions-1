import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.instance_path, "catalog_dir")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 * 1024
app.config['INGESTION_KEY'] = 'dummy'

# db = SQLAlchemy(app)

SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from flaskapp import models
from flaskapp import routes

Base.metadata.create_all(engine)


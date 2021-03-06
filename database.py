# -*- coding: utf-8 -*-
"""
database.py config orm
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:eisti0001@localhost:3306/test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


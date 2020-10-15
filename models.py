# -*- coding: utf-8 -*-
"""
model.py
"""
from sqlalchemy import Table,Boolean, Column, Integer, String, Numeric,SmallInteger,Date,ForeignKey
from sqlalchemy.orm import relationship

from database import Base


play_association_table=Table('play',Base.metadata,
                        Column('id_movie',Integer,ForeignKey('movies.id')),
                        Column('id_actor',Integer,ForeignKey('stars.id')))


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=150), nullable=False)
    year = Column(SmallInteger, nullable=False)
    duration = Column(SmallInteger, nullable=True)
    
    id_director=Column(Integer,ForeignKey('stars.id'))
    director=relationship('Star')
    
    actors=relationship('Star',secondary=play_association_table)

class Star(Base):
    __tablename__ = "stars"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=150), nullable=False)
    birthdate = Column(Date, nullable=True)
    
# -*- coding: utf-8 -*-
"""
schema.py
"""
from typing import Optional,List

from pydantic import BaseModel
from datetime import date

# common Base Class for Movies (abstract class)
class MovieBase(BaseModel):
    title: str
    year: int
    duration: Optional[int] = None

# Movie witout id, only for creation purpose
class MovieCreate(MovieBase):
    pass

# Movie from database with id
class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True

# common Base Class for Movies (abstract class)
class StarBase(BaseModel):
    name: str
    birthdate: Optional[date]

# Movie witout id, only for creation purpose
class StarCreate(StarBase):
    pass

# Movie from database with id
class Star(StarBase):
    id: int

    class Config:
        orm_mode = True
        
class MovieDetail(Movie):
    director: Optional[Star]=None
    actors: List[Star]=[]

class MovieStat(BaseModel):
    year:int
    movie_count:int
    min_duree:Optional[int]
    max_duree:Optional[int]
    avg_duree:Optional[int]
    
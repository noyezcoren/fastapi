"""
file crud.py
manage CRUD and adapt model data from db to schema data to api rest
"""


from typing import Optional,List
from sqlalchemy.orm import Session
from sqlalchemy import extract
from sqlalchemy import func
import models, schemas
from fastapi.logger import logger


def get_Movie(db: Session, Movie_id: int):
    # read from the database (get method read from cache)
    db_movie=db.query(models.Movie).filter(models.Movie.id == Movie_id).first()
    logger.error("Movie retrieved from db:{}; director : {}".format(
        db_movie.title,
        db_movie.director.name if db_movie.director is not None else "no director"))
    logger.error(f"actors: {db_movie.actors}")
    return db_movie

def get_Movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def get_Movies_by_title(db: Session, title: str):
    return db.query(models.Movie).filter(models.Movie.title == title).order_by(models.Movie.year).all()

def get_Movies_by_director_endnames(db: Session, endname: str):
    return db.query(models.Movie).join(models.Movie.director).filter(models.Star.name.like(f'%{endname}%')).order_by(models.Movie.year).all()
    
def get_Movies_by_actor_endnames(db: Session, endname: str):
    return db.query(models.Movie).join(models.Movie.actors).filter(models.Star.name.like(f'%{endname}%')).order_by(models.Movie.year).all()
    

def get_Movies_by_parttitle(db: Session, title: str):
    return db.query(models.Movie).filter(models.Movie.title.like(f'%{title}%')).all()

def get_Movie_year(db: Session, year: int):
    # read from the database (get method read from cache)
    return db.query(models.Movie).filter(models.Movie.year == year).order_by(models.Movie.title).all()

def get_Movies_by_year_range(db: Session, year_min: Optional[int] = None, year_max: Optional[int] = None):
    if year_min is None and year_max is None:
        return None
    elif year_min is None:
        return db.query(models.Movie).filter(models.Movie.year <= year_max).all()
    elif year_max is None:
        return db.query(models.Movie).filter(models.Movie.year >= year_min).all()
    else:
        return db.query(models.Movie) \
                .filter(
                    models.Movie.year >= year_min,
                    models.Movie.year <= year_max) \
                .all()

def create_Movie(db: Session, Movie: schemas.MovieCreate):
    # convert schema object from rest api to db model object
    db_Movie = models.Movie(title=Movie.title, year=Movie.year, duration=Movie.duration)
    # add in db cache and force insert
    db.add(db_Movie)
    db.commit()
    # retreive object from db (to read at least generated id)
    db.refresh(db_Movie)
    return db_Movie

def update_Movie(db: Session, Movie: schemas.Movie):
    db_Movie = db.query(models.Movie).filter(models.Movie.id == Movie.id).first()
    if db_Movie is not None:
        # update data from db
        db_Movie.title = Movie.title
        db_Movie.year = Movie.year
        db_Movie.duration = Movie.duration
        # validate update in db
        db.commit()
    # return updated object or None if not found
    return db_Movie

def delete_Movie(db: Session, Movie_id: int):
     db_Movie = db.query(models.Movie).filter(models.Movie.id == Movie_id).first()
     if db_Movie is not None:
         # delete object from ORM
         db.delete(db_Movie)
         # validate delete in db
         db.commit()
     # return deleted object or None if not found
     return db_Movie



#"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def get_Stars(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Star).order_by(models.Star.birthdate).offset(skip).limit(limit).all()

def get_Star_birthdate(db: Session, bdate:int):
    # read from the database (get method read from cache)
    return db.query(models.Star).filter(extract('year',models.Star.birthdate) == bdate).order_by(models.Star.name).all()

def get_Star_by_name(db: Session, name: str):
    return db.query(models.Star).filter(models.Star.name == name).order_by(models.Star.birthdate).all()

def create_Star(db: Session, Star: schemas.StarCreate):
    # convert schema object from rest api to db model object
    db_Star = models.Star(name=Star.name, birthdate=Star.birthdate)
    # add in db cache and force insert
    db.add(db_Star)
    db.commit()
    # retreive object from db (to read at least generated id)
    db.refresh(db_Star)
    return db_Star

def update_Star(db: Session, Star: schemas.Star):
    db_Star = db.query(models.Star).filter(models.Star.id == Star.id).first()
    if db_Star is not None:
        # update data from db
        db_Star.name = Star.name
        db_Star.birthdate = Star.birthdate
        
        # validate update in db
        db.commit()
    # return updated object or None if not found
    return db_Star

def delete_Star(db: Session, Star_id: int):
     db_Star = db.query(models.Star).filter(models.Star.id == Star_id).first()
     if db_Star is not None:
         # delete object from ORM
         db.delete(db_Star)
         # validate delete in db
         db.commit()
     # return deleted object or None if not found
     return db_Star

def get_Star(db: Session, Star_id: int):
    # read from the database (get method read from cache)
    return db.query(models.Star).filter(models.Star.id == Star_id).first()

def get_Star_by_director_movie_by_title(db:Session,title:str):
    db_movies=db.query(models.Movie).filter(models.Movie.title.like(f'%{title}%')).join(models.Movie.director)
    return [ db_movie.director for db_movie in db_movies ]

def get_Star_by_movie_by_title(db:Session,title:str):
    db_movies=db.query(models.Movie).filter(models.Movie.title.like(f'%{title}%')).join(models.Movie.actors)
    return [ db_movie.actors for db_movie in db_movies ]

def get_Star_by_director_movie(db:Session,movie_id:int):
    db_movie=db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie is not None:
        return db_movie.director
    else :
        return None
      
    
def update_movie_actors(db: Session, movie_id: int, star_id: List[int]):
    stars_list = db.query(models.Star).filter(models.Star.id.in_(star_id)).all()
    db_movie = get_Movie(db=db, movie_id=movie_id)
    if len(stars_list) != len(star_id):
        return None
    db_movie.actors = stars_list
    db.commit()
    return db_movie

def get_movies_count_by_year(db:Session):
    return db.query(models.Movie.year,func.count()).group_by(models.Movie.year).order_by(models.Movie.year).all()

def get_Stars_count_by_year(db:Session):
    query=db.query(models.Star.birthdate,func.count(models.Star.birthdate)).group_by(models.Star.birthdate).order_by(models.Star.birthdate).all()
    return [{"birthdate":i[0],"counter":i[1]} for i in query]
    
def get_movies_stats_by_year(db:Session):
    query = db.query(models.Movie.year,func.count(),func.min(models.Movie.duration),func.max(models.Movie.duration),func.avg(models.Movie.duration)).group_by(models.Movie.year).order_by(models.Movie.year).all()
    return [{"year":i[0],"counter":i[1] ,"mini":i[2], "maxi":i[3], "avg":i[4]} for i in query]


def get_movies_stats_by_director(db:Session,min_count:int=1):
    return db.query(models.Star,func.count(models.Movie.id)).join(models.Movie.director).group_by(models.Star).having(func.count(models.Movie.id)>=min_count).order_by(func.count(models.Movie.id)).all()


def get_stats_by_stars(db: Session,min_count: int):
    return db.query(models.Star, func.count(models.Movie.id),func.min(models.Movie.year),func.max(models.Movie.year))\
        .join(models.Movie.actors)\
        .group_by(models.Star)\
        .having(func.count(models.Movie.id) >= min_count)\
        .order_by(func.count(models.Movie.id))\
        .all()
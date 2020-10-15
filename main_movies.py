from typing import List, Optional ,Set,Tuple, Dict

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

import logging
from fastapi import Depends,FastAPI,HTTPException
from fastapi.logger import logger as fastapi_logger


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
logger=logging.getLogger("uvicorn")
fastapi_logger.handlers=logger.handlers
fastapi_logger.setLevel(logger.level)
logger.error("API started")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/movies/")
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return False

@app.put("/movies/director/", response_model=schemas.MovieDetail)
def update_movie_director(mid: int, sid: int, db: Session = Depends(get_db)):
    db_movie = crud.update_movie_director(db=db, movie_id=mid, director_id=sid)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie or Star not found")
    return db_movie

@app.post("/movies/actor/", response_model=schemas.MovieDetail)
def add_movie_actor(movie_id: int, star_id: int, db: Session = Depends(get_db)):
    """ add one actor to a movie
        mid (query param): movie id
        sid (query param): star id to add in movie.actors
    """
    db_movie = crud.add_movie_actor(db=db, movie_id=movie_id, star_id=star_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie or Star not found")
    return db_movie
    


@app.put("/movies/actors")
def update_movie_actors(mid: int, sid: List[int], db: Session = Depends(get_db)):
    db_movie = crud.update_movie_actors(db=db, movie_id=mid, star_id=sid)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie or Star not found")
    return db_movie


@app.get("/Movies/", response_model=List[schemas.Movie])
def read_Movies(skip: Optional[int] = 0, limit: Optional[int] = 100, db: Session = Depends(get_db)):
    # read Movies from database
    Movies = crud.get_Movies(db, skip=skip, limit=limit)
    # return them as json
    return Movies

@app.get("/Movies/by_id/{Movie_id}", response_model=schemas.MovieDetail)
def read_Movie(Movie_id: int, db: Session = Depends(get_db)):
    db_Movie = crud.get_Movie(db, Movie_id=Movie_id)
    if db_Movie is None:
        raise HTTPException(status_code=404, detail="Movie to read not found")
    return db_Movie

@app.get("/Movies/by_year/{Movie_year}", response_model=List[schemas.Movie])
def read_Movie_year(Movie_year: int, db: Session = Depends(get_db)):
    db_Movie = crud.get_Movie_year(db, year=Movie_year)
    if db_Movie is None:
        raise HTTPException(status_code=404, detail="Movie to read not found")
    return db_Movie


@app.get("/Movies/by_title" , response_model=List[schemas.MovieDetail])
def read_Movies_by_title(n: Optional[str] = None, db: Session = Depends(get_db)):
    # read Movies from database
     Movies = crud.get_Movies_by_title(db=db, title=n)
    # return them as json
     return Movies
    #return n

@app.get("/Movies/by_parttitle", response_model=List[schemas.MovieDetail])
def read_Movies_by_parttitle(n: Optional[str] = None, db: Session = Depends(get_db)):
    # read Movies from database
    Movies = crud.get_Movies_by_parttitle(db=db, title=n)
    # return them as json
    return Movies

@app.get("/Movies/by_year_range", response_model=List[schemas.Movie])
def read_items_by_year_range(ymin: Optional[float] = None,ymax: Optional[float] = None,db: Session = Depends(get_db)):
   # read items from database
   movies = crud.get_Movies_by_year_range(db=db, year_min=ymin, year_max=ymax)
   if movies is None:
       raise HTTPException(status_code=404, detail="Movies year is not in range ")
   # return them as json
   return movies

@app.get("/movies/by_director", response_model=List[schemas.Movie])
def read_Movies_by_director(n: str, db: Session = Depends(get_db)):
    return crud.get_Movies_by_director_endnames(db=db, endname=n)

@app.get("/movies/by_actor", response_model=List[schemas.Movie])
def read_Movies_by_actor(n: str, db: Session = Depends(get_db)):
    return crud.get_Movies_by_actor_endnames(db=db, endname=n)


@app.post("/Movies/", response_model=schemas.Movie)
def create_Movie(Movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    # receive json Movie without id and return json Movie from database with new id
    return crud.create_Movie(db=db, Movie=Movie)

@app.put("/Movies/", response_model=schemas.Movie)
def update_Movie(Movie: schemas.Movie, db: Session = Depends(get_db)):
    db_Movie = crud.update_Movie(db, Movie=Movie)
    if db_Movie is None:
        raise HTTPException(status_code=404, detail="Movie to update not found")
    return db_Movie

@app.delete("/Movies/{Movie_id}", response_model=schemas.Movie)
def delete_Movie(Movie_id: int, db: Session = Depends(get_db)):
    db_Movie = crud.delete_Movie(db, Movie_id=Movie_id)
    if db_Movie is None:
        raise HTTPException(status_code=404, detail="Movie to delete not found")
    return db_Movie

#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@app.get("/Star/by_id/{Star_id}", response_model=schemas.Star)
def read_Star(Star_id: int, db: Session = Depends(get_db)):
    db_Star = crud.get_Star(db, Star_id=Star_id)
    if db_Star is None:
        raise HTTPException(status_code=404, detail="Star to read not found")
    return db_Star

@app.get("/Stars/", response_model=List[schemas.Star])
def read_Stars(skip: Optional[int] = 0, limit: Optional[int] = 100, db: Session = Depends(get_db)):
    # read Stars from database
    Stars = crud.get_Stars(db, skip=skip, limit=limit)
    # return them as json
    return Stars

@app.post("/Stars/", response_model=schemas.Star)
def create_Star(Star: schemas.StarCreate, db: Session = Depends(get_db)):
    # receive json Star without id and return json Star from database with new id
    return crud.create_Star(db=db, Star=Star)

@app.put("/Stars/", response_model=schemas.Star)
def update_Star(Star: schemas.Star, db: Session = Depends(get_db)):
    db_Star = crud.update_Star(db, Star=Star)
    if db_Star is None:
        raise HTTPException(status_code=404, detail="Star to update not found")
    return db_Star

@app.delete("/Stars/{Star_id}", response_model=schemas.Star)
def delete_Star(Star_id: int, db: Session = Depends(get_db)):
    db_Star = crud.delete_Star(db, Star_id=Star_id)
    if db_Star is None:
        raise HTTPException(status_code=404, detail="Star to delete not found")
    return db_Star



@app.get("/Stars/by_year/{star_bdate}", response_model=List[schemas.Star])
def read_Star_birthdate(star_bdate: int, db: Session = Depends(get_db)):
    db_Star = crud.get_Star_birthdate(db, bdate=star_bdate)
    if db_Star is None:
        raise HTTPException(status_code=404, detail="Movie to read not found")
    return db_Star


@app.get("/Stars/by_movie_directed/{movie_id}" , response_model=Optional[schemas.Star])
def read_Star_by_movie_directed(movie_id:int, db: Session = Depends(get_db)):
    Director = crud.get_Star_by_director_movie(db=db,movie_id=movie_id)
    # return them as json
    return Director
    #return n

@app.get("/Stars/by_movie_directed_title/" , response_model=List[schemas.Star])
def read_Star_by_movie_directed_title(t:str, db: Session = Depends(get_db)):
    Director = crud.get_Star_by_director_movie_by_title(db=db,title=t)
    return Director
    #return n

@app.get("/Actors/by_movie_title/" , response_model=List[schemas.Movie])
def read_Star_by_movie(t:str, db: Session = Depends(get_db)):
    Actors = crud.get_Star_by_movie_by_title(db=db,title=t)
    return Actors



@app.get("/movies/count_by_year")
def count_Movies_by_year(db: Session = Depends(get_db)) ->List[Tuple[int,int]] :
    return crud.get_movies_count_by_year(db=db)

@app.get("/Stars/count_by_year")
def count_Stars_by_year(db: Session = Depends(get_db)) ->List[Tuple[int,int]] :
    return crud.get_Stars_count_by_year(db=db)

@app.get("/movies/stats_by_year")
def stats_Movies_by_year(db: Session = Depends(get_db)) ->List[Tuple[int,int,int,int,int]] :
    return crud.get_movies_stats_by_year(db=db)

@app.get("/movies/dico_stats_by_director")
def stats_Movies_by_director(db: Session = Depends(get_db)):
    return crud.get_movies_stats_by_director(db=db)

@app.get("/stars/count_by_stars/")
def read_stats_by_stars(minc: Optional[int]=10, db: Session = Depends(get_db)):
    return crud.get_stats_by_stars(db=db, min_count=minc)


























    #return n

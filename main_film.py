# -*- coding: utf-8 -*


from typing import Optional
from fastapi import FastAPI

from model import Film

app=FastAPI()


@app.get("/films")
def read_all_films():
    return [{"film_id":1,"title": "title1","year": 2020,"duration": 120},{"film_id":2,"title": "title2","year": 2020}]

@app.get("/film/{film_id}")
def read_film(film_id: int, q:Optional[str]=None):
    return {'film_id':film_id,"title": "title_get","year": 2020,"duration": 120}

@app.post("/film")
def post_film(film:Film):
    return {"title": film.title,"year": film.year,"duration": film.duration}

@app.put("/film/{film_id}")
def update_film(film_id: int,film: Film):
    return {'film_id':film_id,'modified':q}

@app.delete("/film/{film_id}")
def delete_film(item_id: int):
    #possible to return the deleted item
    return True

# -*- coding: utf-8 -*


from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool]= None
   

@app.get("/")
def read_root():
    return{"hello word"}

@app.get("/items")
def read_all_items():
    return [{'item_id':2,"name":"tablette"},{'item_id':3,"name":"tablette2"}]

@app.get("/item/{item_id}")
def read_item(item_id: int, q:Optional[str]=None):
    return {'item_id':item_id,"q":q}

@app.post("/item/{item_id}")
def post_item(item:Item):
    return {'item_id':item_id,'new':q}

@app.put("/item/{item_id}")
def update_item(item_id: int,item: Item):
    return {'item_id':item_id,'modified':q}

@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    #possible to return the deleted item
    return True
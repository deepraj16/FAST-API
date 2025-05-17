from fastapi import FastAPI 
from pydantic import BaseModel 
from typing import Optional 
from fastapi.params import Body

#Buliding the app for understanding the flow of CRUD opration in given system 

app=FastAPI()

class Payload(BaseModel): 
    id:int
    title:str 
    content:str 
    published:bool=True
    rating :Optional[int] =None


@app.get('/')
def home(): 
    return {
        "hellow":"ram"
    }

@app.post('/post')
def createpost(payload:Payload): 
    print(payload.dict())
    return {
        "message":"I am working with fast api and they are good", 
        "data" : f"{payload.dict()}"
    }
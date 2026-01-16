from fastapi import FastAPI ,Path,HTTPException,Query
import psycopg2 
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel 
from fastapi.responses import JSONResponse
import json
import random
from time import sleep

#creating a social media platfrom CRUD opreation using fast api for practics us list for 
# storeing the post   

app = FastAPI()
class Post(BaseModel): 
    title :str 
    content :str 
    published : bool=True 

while True :
    try:
        cons = psycopg2.connect(host='localhost',database='fastapi',user="postgres",password="root",port="5432", #second ="5433"
                                cursor_factory=RealDictCursor)
        conn =cons.cursor()
        print("geting connection Succesful !!")
        break

    except Exception as e : 
        print("fail to connect !!")
        print(f"Error : {e}")
        sleep(4)





data =[{"title":"The all is my post","content":"a good day","published" :True,"id":1},
       {"title":"The all is my second","content":"a bad day","published" :True,"id":2}
]

def get_data_from_id(id :int) ->dict : 
    for i in data : 
        if i["id"] == id : 
            return i 
    return {}    

def genrate_id()->int : 
    return random.randint(2,2000)

@app.get('/')
def home_redirect(): 
    """working will all the routes"""
    return { "get":"/all_post",
        "add post" : "/add_post",
        "get_post_with_id":"/all_post/id",
        "get_update":"/post_up",
        "get_delete":"/post_del"
        }
    
@app.get('/all_post')
def all_post():
    
    return JSONResponse({
        "data":data
    })

@app.get("/all_post/{id}")
def get_post(id:int = Path(...,description="get Post when id is passed")):
    post_info=get_data_from_id(id) 
    if post_info is {} : 
        raise HTTPException(status_code=404,detail=f"info of post is not prsent for id {id}")
    
    return JSONResponse({
        "data":post_info
    })

@app.post("/add_post")
def add_post(payload:Post): 
    normal_data = payload.model_dump()
    normal_data["id"]=genrate_id()
    data.append(normal_data)
    return {
        "message":"Data is saved"
    }
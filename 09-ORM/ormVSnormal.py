from fastapi import FastAPI ,Path,HTTPException,Query,status,Depends
import psycopg2 
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel 
from fastapi.responses import JSONResponse
import json
import random
from time import sleep


from sqlalchemy.orm import Session
from database import  engine,get_db
from models import Post    
import models  
from sqlalchemy import text

models.Base.metadata.create_all(bind=engine)

app = FastAPI() 


#creating a social media platfrom CRUD opreation using fast api for practics us list for 
# storeing the post   

app = FastAPI()
class Post(BaseModel): 
    title :str 
    content :str 
    published : bool=True 

data =[{"title":"The all is my post","content":"a good day","published" :True,"id":1},
       {"title":"The all is my second","content":"a bad day","published" :True,"id":2}
]

while True :
    try:
        conns = psycopg2.connect(host='localhost',database='fastapi',user="postgres",password="root",port="5432", #second ="5433"
                                cursor_factory=RealDictCursor)
        cursor =conns.cursor()
        print("geting connection Succesful !!")
        break

    except Exception as e : 
        print("fail to connect !!")
        print(f"Error : {e}")
        sleep(4)


def get_data_from_id(id :int,post:list =data) ->dict : 
    for i in post : 
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
def all_post(db:Session = Depends(get_db())):
    # cursor.execute("Select * from posts")
    # posts =cursor.fetchall()
    posts=db.query(models.Post).all()
    return {
        "data":posts
    }

@app.get("/all_post/{id}")
def get_post(id:int = Path(...,description="get Post when id is passed")):
    cursor.execute("Select * from posts")
    posts =cursor.fetchall()

    post_info=get_data_from_id(id,posts) 
    if post_info == {} : 
        raise HTTPException(status_code=404,detail=f"info of post is not prsent for id {id}")
    
    return {
        "data":post_info
    }


@app.post("/add_post")
def add_post(payload:Post): 
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES( %s ,%s,%s) RETURNING *""",(payload.title,payload.content,payload.published)) 
    post =cursor.fetchone()
    conns.commit()
    return {
        "message":"Data is saved",
        "last_entry":post
    }

@app.get("/all_post2/{id}",status_code=status.HTTP_204_NO_CONTENT)
def get_post(id:int = Path(...,description="get Post when id is passed")):
    cursor.execute("Select * from posts where id = %s",(str(id)))
    post_info =cursor.fetchone()
    
    if not post_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"info of post is not prsent for id {id}")
    
    return {
        "data":post_info
    }

@app.delete("/delete_post/{id}",status_code=status.HTTP_204_NO_CONTENT)  # you can change the staus code for given app
def delete_post(id:int):
    cursor.execute("""delete from posts where id = %s returning *""",(str(id)))
    del_post=cursor.fetchone()
    conns.commit()
    if not del_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Data for id {id} is not present")
    
    return {
        "message":"data is delete"
    }
@app.put("/post/{id}")
def update_data(id:int,payload:Post): 
    cursor.execute("""update posts set title=%s , content=%s ,published=%s where id=%s returning * """,(payload.title,payload.content,payload.published,str(id)))
    update_post = cursor.fetchone()
    conns.commit()
    if update_post is None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Data is not updata")
    return {
        "message":"data is updata",
        "data updated":update_post
    }
    
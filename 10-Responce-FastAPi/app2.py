from fastapi import FastAPI ,Path,HTTPException,Query,status
import psycopg2 
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel 
from fastapi.responses import JSONResponse
import json
import random
from time import sleep
from fastapi.middleware.cors import CORSMiddleware
# using postgres sql 



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Post(BaseModel): 
    title:str 
    content:str 
    published:bool 


@app.on_event("startup")
def startup_db():
    global conn, cursor
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="root",
        port=5432,
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Database connected")



def genrate_id()->int: 
    return random.randint(2,2000)

@app.get("/posts")
def all_post(): 
    cursor.execute("Select * from posts")
    post=cursor.fetchall()
    return{
        "data":post
    }

@app.get("/posts/by/{id}",status_code=status.HTTP_200_OK)
def post_by_id(id:int = Path(...)):
    cursor.execute("select * from posts where id =%s", (id,))
    post_info=cursor.fetchone()

    if not post_info : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="info not found")
    return{
        "data":post_info
    }

@app.post("/add_post")
def add_post(payload:Post): 
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES( %s ,%s,%s) RETURNING *""",(payload.title,payload.content,payload.published)) 
    post =cursor.fetchone()
    conn.commit()
    return {
        "message":"Data is saved",
        "last_entry":post
    }



@app.delete("/delete_post/{id}",status_code=status.HTTP_204_NO_CONTENT)  # you can change the staus code for given app
def delete_post(id:int):
    cursor.execute("""delete from posts where id = %s returning *""",(str(id)))
    del_post=cursor.fetchone()
    conn.commit()
    if not del_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Data for id {id} is not present")
    
    return {
        "message":"data is delete"
    }
@app.put("/post/{id}")
def update_data(id:int,payload:Post): 
    cursor.execute("""update posts set title=%s , content=%s ,published=%s where id=%s returning * """,(payload.title,payload.content,payload.published,str(id)))
    update_post = cursor.fetchone()
    conn.commit()
    if update_post is None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Data is not updata")
    return {
        "message":"data is updata",
        "data updated":update_post
    }
    

from fastapi import FastAPI ,Depends
from database import  get_db,engine
import models
from sqlalchemy import text
from sqlalchemy.orm import Session
from routers import users,posts,auth
app = FastAPI() 

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(posts.router)     
app.include_router(auth.router)           



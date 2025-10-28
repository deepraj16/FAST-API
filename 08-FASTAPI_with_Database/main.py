from fastapi import FastAPI ,Path,HTTPException,Query,status

from psycopg2.extras import RealDictCursor
from pydantic import BaseModel 
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from .database import SessionLocal ,engine 
from . import Model 


Model.Base.metadata.create_all(bind=engine)

app = FastAPI() 

#dependency
def get_db(): 
    db=SessionLocal()
    try : 
        yield db 
    finally : 
        db.close()

@app.post("/test")
def test_post(db:Session =Depends(get_db)): 
    return{
        "stauss":"Scucss"
    }

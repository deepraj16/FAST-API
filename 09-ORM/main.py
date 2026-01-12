from fastapi import FastAPI ,Path,HTTPException,Query,status,Depends


from pydantic import BaseModel 
from fastapi.responses import Response

from sqlalchemy.orm import Session
from database import  engine,get_db
  
import models  
from sqlalchemy import text
import schemas
models.Base.metadata.create_all(bind=engine)

app = FastAPI() 


@app.get("/")
@app.get("/check_db")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "connected", "message": "Database connection successful "}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@app.get("/data",status_code=status.HTTP_200_OK)
def data(db : Session = Depends(get_db)):
    try: 
        post =db.query(models.Post).all()
        return {
            "data":post
        }
    except HTTPException as e : 
        return {
            "message":"not successful error {e}"
        }
    
@app.post("/new_post")
def add_post(payload:schemas.posts,db:Session=Depends(get_db)):
    post_data = models.Post(title=payload.title , content=payload.content,published=payload.published) 
    db.add(post_data)
    db.commit()
    db.refresh(post_data)
    return {
        "data":post_data
    }


# when you have more number of colums and you have to work with it 
@app.post("/new_post_op")
def new_post_op(payload:schemas.posts,db:Session=Depends(get_db)): 
    new_data =models.Post(**payload.model_dump()) 
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return{
        "data":new_data
    }


@app.get("/data/{id}")
def data_by_id(id:int , db:Session=Depends(get_db)): 
    filter_data = db.query(models.Post).filter(models.Post.id ==id).first()
    if not filter_data: 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the data is not found for id {id}")
    
    return {
        "data":filter_data
    }


@app.delete("/data/{id}")
def delete_data(id : int ,db:Session=Depends(get_db)): 
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None : 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/data/{id}")
def update_post(id:int ,post : schemas.posts,db :Session=Depends(get_db)): 
    post_update =db.query(models.Post).filter(models.Post.id == id)
    post_query=post_update.first()
    if not post_query : 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post_update.update(**post.model_dump(),synchronize_session=False)
    db.commit()
    return {
        "message":"succesful"
    }


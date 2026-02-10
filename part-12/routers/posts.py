          
from fastapi import HTTPException,status,Depends,APIRouter
from typing import List
from fastapi.responses import Response
import schemas 
from database import  get_db,engine
import models
from sqlalchemy import text
from sqlalchemy.orm import Session
from utils import hashing
import outh

router = APIRouter(
    prefix="/data"
)


    

@router.get("",status_code=status.HTTP_200_OK,response_model=List[schemas.Post_Responce])
def data(db : Session = Depends(get_db)): 
        post =db.query(models.Post).all()
        return post
        
    
@router.post("",response_model=schemas.Post_Responce)
def add_post(payload:schemas.posts,db:Session=Depends(get_db) ,user_id :int =Depends(outh.get_current_user)):
    
    post_data = models.Post(title=payload.title , content=payload.content,published=payload.published,user_id=payload.user_id) 
    db.add(post_data)
    db.commit()
    db.refresh(post_data)
    print(user_id)
    print(type(user_id))
    return post_data

# when you have more number of colums and you have to work with it 
@router.post("/op",response_model=schemas.Post_Responce)
def new_post_op(payload:schemas.posts,db:Session=Depends(get_db)): 
    new_data =models.Post(**payload.model_dump()) 
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


@router.get("/{id}",response_model=schemas.Post_Responce)
def data_by_id(id:int , db:Session=Depends(get_db)): 
    filter_data = db.query(models.Post).filter(models.Post.id ==id).first()
    if not filter_data: 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the data is not found for id {id}")
    
    return filter_data


@router.delete("/{id}",)
def delete_data(id : int ,db:Session=Depends(get_db),current_user =Depends(outh.get_current_user)): 
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None : 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND ,  detail="Post not found")

    if post.first().user_id != current_user.id : 
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not authorized to perform requested action")
    

    post.delete(synchronize_session=False)
    db.commit()
    print(current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # when you have to return empty response you can use this

@router.put("/{id}")
def update_post(id:int ,post : schemas.posts,db :Session=Depends(get_db),current_user  =Depends(outh.get_current_user)): 
    post_update =db.query(models.Post).filter(models.Post.id == id)
    post_query=post_update.first()
    if not post_query : 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post_update.update(post.model_dump(),synchronize_session=False)
    db.commit()
    
   
    return "updated successfully"  

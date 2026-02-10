from fastapi import HTTPException,status,Depends,APIRouter
from typing import List
from fastapi.responses import Response
import schemas 
from database import  get_db,engine
import models
from sqlalchemy import text
from sqlalchemy.orm import Session
from utils import hashing

router =APIRouter(
    prefix="/users"
)

@router.get("",status_code=status.HTTP_200_OK,response_model=List[schemas.UsersResponce])
def createUser(db:Session=Depends(get_db)):
    All_Users=db.query(models.Users).all()
    return All_Users



@router.post("",status_code=status.HTTP_201_CREATED,response_model=schemas.UsersResponce)
def CreateUser(users: schemas.Users_,db: Session = Depends(get_db)):
  
    existing_user_email = db.query(models.Users)\
                      .filter(models.Users.email == users.email)\
                      .first()
    
    existing_user_username=db.query(models.Users).filter(models.Users.username == users.username).first()
    if existing_user_email  :
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    if existing_user_username : 
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username is not avilable"
        )
    hased_password=hashing(users.password)
    users.password = hased_password

    new_user = models.Users(**users.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/id/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UsersResponce)
def get_user_by_id(id:int,db:Session = Depends(get_db)): 
    user_data = db.query(models.Users).filter(models.Users.id == id).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="user not found")
    
    return user_data


@router.get("/username/{username}",status_code=status.HTTP_200_OK,response_model=schemas.UsersResponce)
def get_user_by_id(username:str,db:Session = Depends(get_db)): 
    user_data = db.query(models.Users).filter(models.Users.username == username).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="user not found")
    
    return user_data


@router.put("/{id}")
def update_post(id:int ,post : schemas.posts,db :Session=Depends(get_db)): 
    post_update =db.query(models.Users).filter(models.Users.id == id)
    post_query=post_update.first()
    if not post_query : 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post_update.update(**post.model_dump(),synchronize_session=False)
    db.commit()
    return {
        "message":"succesful"
    }

@router.delete("/{id}")
def get_delete(id:int,db:Session=Depends(get_db)):
    post = db.query(models.Users).filter(models.Users.id == id)
    if post.first() == None : 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT )


# get the users posts which he/she had created at given postion to undestand the relations betweens the tables
@router.get("/posts/{id}",response_model=List[schemas.Post_Responce])
def get_user_posts(id:int,db:Session=Depends(get_db)):
    user_posts = db.query(models.Post).filter(models.Post.user_id == id).all()
    if not user_posts : 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return user_posts
from fastapi import APIRouter ,HTTPException,status,Depends
from database import engine,get_db 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models 
import schemas 
import utils 
import outh



router = APIRouter(tags=["Authntication"])

@router.post("/login")
def login(user_cre : schemas.UserLogin , db:Session=Depends(get_db)): 
    user_info =db.query(models.Users).filter(models.Users.email==user_cre.email).first()
    
    if not user_info: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Crediction")
    
    if not utils.verify(user_cre.password,user_info.password) : 
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Password")
    
    access_token = outh.create_access_token(data ={"user_id":user_info.id ,"user_name":user_info.username})

    return {"access_token":access_token ,"token_type":"bearer"}


@router.post("/loginFrom")
def loginFrom(user_cre : OAuth2PasswordRequestForm =Depends() , db:Session=Depends(get_db)): 
    user_info =db.query(models.Users).filter(models.Users.email==user_cre.username).first()
    
    # OAuth2PasswordRequestForm contains username and password fields
    # Here, we use user_cre.username to get the email
    # The rest of the logic remains the same
    if not user_info: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Crediction")
    
    if not utils.verify(user_cre.password,user_info.password) : 
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Password")
    
    access_token = outh.create_access_token(data ={"user_id":user_info.id ,"user_name":user_info.username})

    return {"access_token":access_token ,"token_type":"bearer"}
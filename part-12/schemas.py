
from pydantic import BaseModel
from pydantic import ConfigDict,EmailStr
from datetime import datetime
from typing import Optional


class Users_(BaseModel):
    email:EmailStr
    username:str 
    password:str 


class UsersResponce(BaseModel): 
    model_config=ConfigDict(from_attributes=True) # it is used becoues pydinat only undertand dict but 
    # we are working with sql dic so for configuring it we use ConfigDict
    id:int
    email:EmailStr
    username:str 


class posts(BaseModel): 
    title :str 
    content :str 
    published : bool=True 
    user_id : int
    
    model_config = ConfigDict(from_attributes=True)
    
    

class PostCreated(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title :str 
    content :str 
    published : bool=True 
    


class Post_Responce(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    title :str 
    content :str 
    published : bool=True 
    created_at :datetime
    owner : UsersResponce 
    user_id : int
 
class UserLogin(BaseModel): 
    email :EmailStr
    password:str 


class Token(BaseModel):
    access_token :str 
    password:str 

class TokenData(BaseModel): 
    id: Optional[int] =None
    





from jose import JWTError,jwt
from datetime import datetime,timedelta
import schemas

from fastapi import Depends,status,HTTPException 
from fastapi.security import OAuth2PasswordBearer 



oauth2_scheme =OAuth2PasswordBearer(tokenUrl="loginFrom")
#serat key 
#algo
#expoisre time 

SECREAT_KEY="hellow"
ALGORITHIM="HS256"
TIME_EX =30

def create_access_token(data:dict):
    to_encode =data.copy()
    
    expire =datetime.utcnow() + timedelta(minutes=TIME_EX)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECREAT_KEY,algorithm=ALGORITHIM)

    return encoded_jwt


def verify_access_token(token:str ,credentials_exception): 
    try:
        payload = jwt.decode(token , SECREAT_KEY,algorithms=[ALGORITHIM])

        id:str = payload.get("user_id")

        if id is None :
            raise credentials_exception 
        
        token_data = schemas.TokenData(id=id)

    except JWTError :
        raise credentials_exception
    
    return token_data

def get_current_user(token :str=Depends(oauth2_scheme)):
    credentials_exception =HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,
                                         detail=f"Could not vaild credtional",
                                         headers={"WWW-Authenticate": "Bearer"}
    )
    
    return  verify_access_token(token,credentials_exception)

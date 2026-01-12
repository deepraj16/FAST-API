
from pydantic import BaseModel

# class posts(BaseModel): 
#     title :str 
#     content :str 
#     published : bool=True 

class PostCreated(BaseModel):
    title :str 
    content :str 
    published : bool=True 

class PostUpdate(PostCreated): 
    pass 




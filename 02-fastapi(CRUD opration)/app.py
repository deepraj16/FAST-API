from fastapi import FastAPI ,status,HTTPException
from pydantic import BaseModel 
from fastapi.responses import JSONResponse
from typing import Optional
from random import randrange
app = FastAPI()


class Payload(BaseModel): 
    title:str 
    content:str
    pubished:bool = True
    rating:Optional[int] = None



def find_post(id): 
    for i in my_post: 
        if(i["id"]==int(id)): 
            return i
    return None  

def find_the_post(id): 
    for i,p in enumerate(my_post): 
        if(p["id"]==id):
            return i
    return None    




my_post=[{"title":"my first post","content":"working with ram","pubished":True,"id":1},{"title":"nice day","content":"hellow nidi","pubished":True,"id":2}]

@app.get('/')
async def home(): 
    return {'message':'Hellow world'}

@app.get('/post')
def get_post():
    return {'data':my_post}
        

@app.post('/post',status_code=status.HTTP_201_CREATED)
def post_meassage(new_post:Payload): 
    pay=new_post.dict()
    pay["id"]=randrange(2,340000)
    my_post.append(pay)
    return {
        'message': f"I am working in post method. Title:",
        'received_data': new_post.dict()
    }


from fastapi import Response
@app.get("/post/{id}")
def get_post(id:int,response:Response):
    print(type(id))
    data=find_post(id) 
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the {id} not found in the data")
    

    return {
        "post detail":f"here data of {id}",
        "data":data
    }


@app.get("/postlast")
def get_lastpost():
    lastpost=my_post[len(my_post)-1]
    return{
        "last post":lastpost
    } 


# @app.delete("/post/{id}")
# def delete_post(id:int): 
#     post_index=find_the_post(id)
#     my_post.pop(post_index)
#     return{"message":"post is deleted"}

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int): 
    post_index=find_the_post(id) 
    if not post_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    my_post.pop(post_index) 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}")
def updata_post(id:int,post:Payload): 
    print(post)
    print(id)
    index =find_the_post(id)
    if  index==None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="{id} is not found")
    post_dict=post.dict() 
    post_dict["id"]=id 
    my_post[index]=post_dict
    return{"update":"update the post", "new-post":f"{post_dict}"}
    
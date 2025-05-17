from fastapi import FastAPI 
from pydantic import BaseModel 
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()


class Payload(BaseModel): 
    title:str 
    content:str
    pubished:bool = True
    rating:Optional[int] = None


@app.get('/')
async def home(): 
    return {'message':'Hellow world'}

@app.post('/post')
def post_meassage(new_post:Payload): 
    pay=new_post
    print(new_post.dict())
    return {
        'message': f"I am working in post method. Title: {new_post.title}",
        'received_data': new_post.dict()
    }






















# @app.get('/post/{post_id}') 
# def get_post(post_id:int): 
#     return {
#         'post_id': post_id
#     }
# @app.put('/post/{post_id}')
# def update_post(post_id:int, post:Payload): 
#     return {
#         'post_id': post_id,
#         'data': post
#     }
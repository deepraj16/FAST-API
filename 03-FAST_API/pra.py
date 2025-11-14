from fastapi import FastAPI 
from fastapi.params import Body 
from typing import Optional 
from pydantic import BaseModel 

app=FastAPI()

@app.post('/post')
def create(payload: dict=Body(...)):
    pay=payload
    return {"message":f"hellow {pay['title']}" }




# @app.get("/post/{id}")
# def get_post(id:int):
#     print(type(id))
#     data=find_post(id) 
#     return {
#         "post detail":f"here data of {id}",
#         "data":data
#     }

# stats code for given applaction 
# 404 -respondce not found it is a clint error which occrance    

def find_post(id):
    pass



from fastapi import Response
@app.get("/post/{id}")
def get_post(id:int,response:Response):
    print(type(id))
    data=find_post(id) 
    if not data: 
        response.status_code=404

    return {
        "post detail":f"here data of {id}",
        "data":data
    }

from fastapi import FastAPI 
from fastapi.params import Body

app=FastAPI()

@app.get('/') 
async def home(): 
    return {'hellow' : "Deepraj"}

@app.post('/createPost')
def create_post() :  
    return {"meassage" : "hellow my name is deepraj" }

@app.post('/post')
def postwork(payload: dict=Body(...)): 
    pay=payload 
    print(pay)
    return  { "in post": f"title: {pay['message']} content: {pay['title']}" }
from fastapi import FastAPI 
from fastapi.params import Body 


app = FastAPI()

@app.get('/')
async def home(): 
    return {'message':'Hellow world'}

@app.post('/post')
def post_meassage(payload:dict =Body(...)): 
    pay=payload
    print(pay)
    return {'message':f"i am working inpost method body tile{pay.title}"}
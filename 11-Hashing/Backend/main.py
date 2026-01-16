from pydantic import BaseModel 
from fastapi import FastAPI ,HTTPException,Path
from fastapi.responses import JSONResponse 
from Pydiantic import Student_Id
from raw_data import load_data

app = FastAPI()

#Student CRUD Oprations for given code 
@app.get("/")
def home():
    return {
        "data" : "Hellow working on student mangment system !!"
    }

@app.get("/views")
def student():
    try: 
        data =load_data()
    except FileExistsError as e : 
        raise     
    return {
        "data":data
    }

@app.get("/student/{stu_id}")
def get_student(stu_id :str = Path(...,description="The give route take student id and then print the detalis of it")):
    """the student view from given system"""
    data=load_data()
    if stu_id not in data.keys(): 
        raise HTTPException(status_code=404,detail="Data Not Found !!")
    
    info_of_student=data[stu_id] 
    return {
        "data":info_of_student
    }





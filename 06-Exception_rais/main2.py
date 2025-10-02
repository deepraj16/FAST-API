from fastapi import FastAPI ,Path,HTTPException
from fastapi import Query
import json
import os

app = FastAPI()

DATA_FILE="patients2.json"
def load_data():
    try :
        if not os.path.exists(DATA_FILE): 
            return {}
        with open(DATA_FILE,"r") as f: 
            data = json.load(f)
            return data
    except FileExistsError : 
        raise FileNotFoundError("No data founded")
    

def get_citys()-> dict :
    data =load_data()
    info = {}
    for key,val in data.items(): 
        if val["city"] not in info.keys(): 
            info[val["city"]]=[key]
        else : 
            k=info[val["city"]]
            k.append(key)
            info[val["city"]]=k

    return info            




@app.get("/")
@app.get("/home")
def home():
    return{
        "message":"Wellcome to Patients mangment system"
    }

@app.get("/views")
def views():
    data = load_data()
    return {
        "data":data
    }


@app.get("/citys")
def citys():
    data = get_citys()
    return{
        "data" : data
    }        

@app.get("/views/{patient_id}")
def get_patient_by_id(patient_id : str =Path(...,description="GET THE INFO OF PATIENTS BY ID",example="P005")):
    data =load_data()
    if patient_id not in data.keys():
        raise HTTPException(status_code=404,detail="DATA NOT FOUND")
    
    INFO = data[patient_id]
    return{
        "data":INFO
    }
@app.get("/sort")
def sort_by(sorted_by : str =Query(...,description="Working on sorting  [height , weight , age, bmi ]")
            ,order: str=Query("asc",description="it will set the data in decs or acs")): 
    
    valid_fields =["height","weight","age","bmi"]
    if sorted_by not in valid_fields :
        raise HTTPException(status_code=400,detail="not a vaild fild for sorting")
    
    if order not in ["desc","asc"]: 
        raise HTTPException(status_code=400 ,detail="not a vaild sorting order")
    
    data=load_data()
    sort_order = True if order == "desc" else False 
    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0) , reverse=sort_order)

    return{
        "data":sorted_data
    }
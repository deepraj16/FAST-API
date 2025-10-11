from fastapi import FastAPI ,Path,Query ,HTTPException
import json 
import os 

FILE_NAME="patients2.json"

def load_data()->dict :
    try:
        if not os.path.exists(FILE_NAME) : 
            raise FileExistsError("File not exist")

        with open(FILE_NAME,"r") as f: 
            data = json.load(f)
            return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error {e}")
    except FileExistsError as e: 
        raise FileExistsError(f"ERROR {e}")

app = FastAPI()

@app.get("/")
def home(): 
    return {
        "hellow":"wellcome"
    }

@app.get('/views/{patient_id}')
def get_patient_byID(patient_id:str = Path(...,description="get patients by id",example="P001")): 
    data = load_data()
    return{
        "data":data
    }


@app.get('/sort')
def sort_by_(sort_by :str = Query(...,description="working sorted by height or weight"),
             order_by:str=Query("desc",description="working with way of sorting")):
    if sort_by not in ["height","weight","bmi"]:
        raise HTTPException(status_code=400,detail="Wrong user input")
    
    if order_by not in ["desc","asc"]: 
        raise HTTPException(status_code=400,detail="Worong way of order")
    
    data =load_data()
    
    order_ = True if order_by == "desc" else False
    sorted_data =sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=order_)

    return{
        "data":sorted_data
    }





    


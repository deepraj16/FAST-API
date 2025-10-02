import json 
import os
DATA_FILE = "patients.json"

def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            return []

        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, list):  
                raise ValueError("Invalid data format, expected a list")
            return data
    except FileNotFoundError:
        raise FileNotFoundError("no data is present")
 
def only_doctor(): 
    doc=[]
    data=load_data()
    for i in data : 
        doc.append({i['id']:i["doctor"]})
    return doc    

# Save patients data safely
def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise FileNotFoundError("no data is persent")
    
def check_data(info:dict) -> bool :
    if len(info)==7: 
        return True   
    return False    

def load_Info(id: int) -> dict : 
    data = load_data()
    for i in data: 
        if i["id"] == id : 
            return i
    return {}    



import os
import json

FILE_DIR="students.json"
def load_data()->dict :
    
    if not os.path.exists(FILE_DIR):
        raise FileExistsError("The File not found !!")
    
    try:
        with open(FILE_DIR,"r") as f: 
            data =json.load(f)
            return data
    except FileNotFoundError as e:
        print(e)

    return data 




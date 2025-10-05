from pydantic import BaseModel
from typing import List,Dict

class Patient(BaseModel): 
    name:str 
    age:int
    weight:float 
    married : bool 
    allergies: List[str]
    contact_details : Dict[str,str]

def Insert_into_database(patient : Patient): 
    """Inserting in database """
    print(patient.name)
    print(patient.age)

def Updata_into_database(patient : Patient): 
    """ Updata in database """
    print(patient.name)
    print(patient.age)


patient_info = {'name':'nitish','age':30,"weight":7.8,"married":True,"allergies":["rr","rrr"],}

pat1 = Patient(**patient_info)
Insert_into_database(pat1)    
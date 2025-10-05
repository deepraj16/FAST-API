from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

#making the fild's of given data in given time for the normal form
#type validation
class Patient(BaseModel): 
    name:Annotated[str,Field(max_length=50,title="Name of the patient",description="")]
    age:int = Field(gt=0,ls=120)
    mail:EmailStr
    weight:float =Field(gt=0,ls=0,strict=True)
    married : bool =False
    allergies: Optional[List[str]] = None
    contact_details : Optional[Dict[str,str]] =Field(max_length=10)

def Insert_into_database(patient : Patient): 
    """Inserting in database """
    print(patient.name)
    print(patient.age)

def Updata_into_database(patient : Patient): 
    """ Updata in database """
    print(patient.name)
    print(patient.age)


patient_info = {'name':'nitish','mail':"deeprajautade@gmail.com",'age':30,"weight":7.8,"married":True,"allergies":["rr","rrr"],"contact_details":{"om":"9890848703"}}

pat1 = Patient(**patient_info)
Insert_into_database(pat1)    


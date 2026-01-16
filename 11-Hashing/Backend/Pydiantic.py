
from pydantic import BaseModel 
from typing import List 

class Student_Id(BaseModel): 
    id:int
    

stu ={"id":4}
student_1 = Student_Id(**stu)    
print(student_1)
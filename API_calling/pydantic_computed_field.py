from pydantic import BaseModel, computed_field,Field
from typing import List, Dict,Optional,Annotated

class Patient(BaseModel):
    name:str
    age:int= Field(gt=0, lt=80)
    weight:float
    height:Annotated[float,Field(default=None)]
    married:Annotated[bool,Field(default=0)]
    allergies:Optional[List[str]]=None
    contact: Optional[Dict[str,str]]=None
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

def insert_details(Patient:Patient):
    print(Patient.name)
    print(Patient.age)
    print(Patient.weight)
    print(Patient.height)
    print(Patient.contact)
    print(Patient.bmi)
    
patient_info= {'name':'Yatharth','age':65,'weight':50,'contact':{'emergency':"7418529630"},'height':1.67}
patient1=Patient(**patient_info)

insert_details(patient1)
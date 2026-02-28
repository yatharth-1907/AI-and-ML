from pydantic import BaseModel, model_validator,Field
from typing import List, Dict,Optional,Annotated

class Patient(BaseModel):
    name:str
    age:int= Field(gt=0, lt=80)
    weight:float
    height:Annotated[float,Field(default=None)]
    married:Annotated[bool,Field(default=0)]
    allergies:Optional[List[str]]=None
    contact: Optional[Dict[str,str]]=None
    
    @model_validator(mode='after')
    # @classmethod
    def validate_emergency(cls, model):
        if model.age>60 and 'emergency' not in model.contact:
            raise ValueError(" Age is Greater than 60 there should be Emergency number")
        return model

def insert_details(Patient:Patient):
    print(Patient.name)
    print(Patient.age)
    print(Patient.weight)
    print(Patient.height)
    print(Patient.contact)
    
patient_info= {'name':'Yatharth','age':65,'weight':50,'contact':{'emergency':"7418529630"}}
patient1=Patient(**patient_info)

insert_details(patient1)
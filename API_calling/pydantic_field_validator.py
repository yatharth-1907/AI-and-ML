from pydantic import BaseModel, field_validator,EmailStr,AnyUrl,Field
from typing import List,Dict,Annotated,Optional

class patient(BaseModel):
    name:str
    age:int=Field(gt=0, le=70)
    weight:float
    height:Optional[float]=None
    linkedin_id:AnyUrl
    email:Optional[EmailStr]=None
    allergies:Annotated[List[str],Field(default=None,description="here you have to write the allergies which the patient have.")]
    contact:Optional[Dict[str,str]]=None
    
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        domain=value.split("@")[-1]
        valid=['icici.com','sbi.com']
        if domain not in valid:
            raise ValueError("Not a valid Domain")
        return value
    
def insert_details(Patient:patient):
    print(Patient.name)
    print(Patient.age)
    print(Patient.allergies)
    print(Patient.email)
    
patient_info={'name':"Yatharth",'age':21,'weight':50,'contact':{"number":'9424852525'},'linkedin_id':"http:\linkedin.com",'email':'abcde@sbi.com'}

patient1=patient(**patient_info)

insert_details(patient1)
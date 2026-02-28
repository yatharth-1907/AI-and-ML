from pydantic import BaseModel

class address(BaseModel):
    city:str
    state:str
    pin:str

class patient(BaseModel):
    name:str
    age:int
    gender:str='M'
    address:address
    
address_dict={'city':"dewas",'state':'MP','pin':'455001'}

address1=address(**address_dict)

patient_info={'name':'Yatharth','age':21,'address':address1}

patient1=patient(**patient_info)

temp=patient1.model_dump(exclude_unset=True)

print(temp)
print(type(temp))
    

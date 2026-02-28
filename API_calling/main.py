from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional

def load_file():
    with open("API_calling/patients.json",'r') as f:
        data= json.load(f)
    return data

def save_data(data):
    with open("API_calling/patients.json",'w') as f:
        json.dump(data,f)

app=FastAPI()

class patient(BaseModel):
    id:str = Field(..., description="Patient ID", example="P001")
    name:Annotated[str,Field(...,description="Write the name of the patient")]
    city:Annotated[str, Field(..., description="add the city of the paitient")]
    age:Annotated[int, Field(...,description="add the age of the patient",gt=0)]
    gender:Annotated[Literal['Male','Female','other'],Field(...,description="you have to write the gender of the patient" )]
    height:Annotated[float,Field(..., gt=0)]
    weight:Annotated[float,Field(..., gt=0)]
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def vedict(self)->str:
        if self.bmi <18.5:
            return 'Underweight'
        elif 18.5<=self.bmi<=24.5:
            return 'Normal' 
        else:
            return 'Obese'
        
class patientUpdate(BaseModel):
    id: Optional[str] = Field(None, description="Patient ID", example="P001")
    name: Annotated[Optional[str], Field(None, description="Write the name of the patient")]
    city: Annotated[Optional[str], Field(None, description="add the city of the paitient")]
    age: Annotated[Optional[int], Field(None, description="add the age of the patient", gt=0)]
    gender: Annotated[Optional[Literal['Male', 'Female', 'other']], Field(None, description="you have to write the gender of the patient")]
    height: Annotated[Optional[float], Field(None, gt=0)]
    weight: Annotated[Optional[float], Field(None, gt=0)]
        
    
@app.get("/")
def hello():
    return ('hello world')

@app.get("/test")
def test():
    return("this is a test message.")

@app.get('/view')
def view():
    data= load_file()
    return(data)

@app.get('/patient/{patient_id}')
def get_details(patient_id: str = Path(description="Patient Id in which is in database",example='P001')):
    data= load_file()
    
    if patient_id not in data:
        return data[patient_id]
        raise HTTPException(status_code=404,detail="Patient ID not found")

@app.get('/sort')
def sort(sort_by:str= Query(...,description="Sort on the bsis of weight,height,bmi"),order:str=Query('asc',description="Insert asc or desc")):
    valid_field= ['height','weight','bmi']
    if sort_by not in valid_field:
        raise HTTPException(status_code=400,detail="Invalid field selected from {valid_field}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid order selected")
    data= load_file()
    sort_order= True if order=='desc'else False
    
    sorted_data= sorted(data.values(),key= lambda x:x.get(sort_by,0),reverse=sort_order)
    
    return sorted_data

@app.post('/create')
def create_patient(Patient:patient):
    #load existing date
    data= load_file()
    
    # check if patient already exist
    if Patient.id in data:
        raise HTTPException(status_code=400,detail="Patiend detail already exist")
    # add new data
    data[Patient.id]=Patient.model_dump(exclude='id')
    
    #save the model 
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message': 'patient added successfully'})

@app.put("/edit/{patient_id}")
def update_patient(patient_id:str, patient_update: patientUpdate):
    
    data = load_file()
    
    if patient_id not in data:
        raise HTTPException(status_code=400,detail="Patient not found")
    
    existing_patient=data[patient_id]
    
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
    
    for key,value in updated_patient_info.items():
        existing_patient[key]=value
    
    # My current existing_patient does not contain the patient id and once we update the data we need to recalculate the Bmi and verdict
    
    # existing_patient -> pydnatic object -> update bmi+verdict
    existing_patient['id']=patient_id
    gender_value = existing_patient.get('gender')
    if isinstance(gender_value, str):
        normalized_gender = gender_value.lower()
        gender_map = {'male': 'Male', 'female': 'Female', 'other': 'other'}
        existing_patient['gender'] = gender_map.get(normalized_gender, gender_value)
    patient_pydantic_obj= patient(**existing_patient)
    
    existing_patient=patient_pydantic_obj.model_dump(exclude='id')
    
    data[patient_id]=existing_patient
    
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message': 'Data Updated'})

@app.delete('/delete_patient/{pataient_id}')
def delete_patient(patient_id:str):
    
    data= load_file()
    
    if patient_id not in data:
        raise HTTPException(status_code=400,detail="Patient not found")
    
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message':'Data Deleted Successfully'})
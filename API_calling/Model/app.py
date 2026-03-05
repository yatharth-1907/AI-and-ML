from fastapi import FastAPI, HTTPException,Query,Path
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
import pickle
from pathlib import Path
import pandas as pd


model_path = Path(__file__).parent / "model.pkl"
with model_path.open("rb") as f:
    model= pickle.load(f)
    
app= FastAPI()


class UserInput(BaseModel):
    
    age:Annotated[int,Field(...,description="You have to write your age")]
    gender:Annotated[Literal['Male','Other','Female'],Field(...,description="Add your age")]
    academic_level:Annotated[Literal['Postgraduate','High School','Undergraduate'],Field(...,description='add your academic level')]
    study_hours:Annotated[float,Field(...,description='Enter your hours you study')]
    self_study_hours:Annotated[float,Field(...)]
    online_classes_hours:Annotated[Optional[float],Field(2.0)]
    social_media_hours:Annotated[float,Field(...)]
    gaming_hours:Annotated[Optional[float],Field(1.0)]
    sleep_hours:Annotated[float,Field(...)]
    screen_time_hours:Annotated[float,Field(...)]
    exercise_minutes:Annotated[float,Field(...)]
    caffeine_intake_mg:Annotated[Optional[float],Field(251.0)]
    part_time_job:Annotated[int,Field(...,ge=0,le=1)]
    upcoming_deadline:Annotated[int,Field(...)]
    internet_quality:Annotated[Literal['Good','Average','Poor'],Field(...)]
    
    
@app.post('/predict')
def predict_marks(data:UserInput):
    input_df= pd.DataFrame([{
        'age':data.age,
        'gender':data.gender,
        'academic_level':data.academic_level,
        'study_hours':data.study_hours,
        'self_study_hours':data.self_study_hours,
        'online_classes_hours':data.online_classes_hours,
        'social_media_hours':data.social_media_hours,
        'gaming_hours':data.gaming_hours,
        'sleep_hours':data.sleep_hours,
        'screen_time_hours':data.screen_time_hours,
        'exercise_minutes':data.exercise_minutes,
        'caffeine_intake_mg':data.caffeine_intake_mg,
        'part_time_job':data.part_time_job,
        'upcoming_deadline':data.upcoming_deadline,
        'internet_quality':data.internet_quality 
    }])
    prediction=model.predict(input_df)
    # model.predict returns ndarray; convert to JSON-serializable scalar
    prediction_value = float(prediction[0]) if getattr(prediction, "__len__", None) else float(prediction)
    return JSONResponse(status_code=200,content={'Marks':prediction_value})
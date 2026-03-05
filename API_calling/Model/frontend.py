import streamlit as st
import requests

App_url= "http://127.0.0.1:8000/predict"

st.title("Marks Predictor")
st.markdown("Enter details below")

#input field

age= st.number_input("Age", min_value=16, max_value=70,value=18)
gender=st.selectbox("Gender",options=['Male','Female','Other'])
academic_level=st.selectbox("Academic level",options=['Postgraduate','High School','Undergraduate'])
study_hours= st.number_input('Study hours',min_value=0.0, max_value=24.0, value=0.0)
self_study_hours=st.number_input('Self study hours', min_value=0.0, max_value=24.0, value=0.0)
online_classes_hours=st.number_input("Online classes hours",min_value=0.0, max_value=24.0, value=0.0)
social_media_hours=st.number_input(" Social media hours",min_value=0.0, max_value=24.0, value=0.0)
gaming_hours=st.number_input("Gaming Hours",min_value=0.0, max_value=24.0, value=0.0)
sleep_hours=st.number_input("Sleep hours ",min_value=0.0, max_value=24.0, value=0.0)
screen_time_hours= st.number_input(" Screen time hours",min_value=0.0, max_value=24.0, value=0.0)
exercise_minutes= st.number_input("Exercise in Minutes",min_value=0.0, max_value=14400.0, value=0.0)
caffeine_intake_mg=st.number_input("Caffeine Intake in mg",min_value=0.0, max_value=1000.0, value=251.0)
part_time_job= st.number_input("Part time job ( Answer in 0 or 1",min_value=0, max_value=2, value=0)
upcoming_deadline= st.number_input(" Any upcoming deadline (answer in 0 or 1)",min_value=0, max_value=2 , value=0)
internet_quality= st.selectbox("Internet Quality", options=['Good','Average','Poor'])

if st.button("Predict marks"):
    input_data= {
        'age':age,
        'gender':gender,
        'academic_level':academic_level,
        'study_hours':study_hours,
        'self_study_hours':self_study_hours,
        'online_classes_hours':online_classes_hours,
        'social_media_hours':social_media_hours,
        'gaming_hours':gaming_hours,
        'sleep_hours':sleep_hours,
        'screen_time_hours':screen_time_hours,
        'exercise_minutes':exercise_minutes,
        'caffeine_intake_mg':caffeine_intake_mg,
        'part_time_job':part_time_job,
        'upcoming_deadline':upcoming_deadline,
        'internet_quality':internet_quality
    }
    
    try:
        response = requests.post(App_url,json=input_data)
        result=response.json()
        
        if response.status_code==200:
            prediction = result.get('Marks')
            st.success(f"predicted Marks: **{prediction}**")
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)
            
    except requests.exceptions.ConnectionError:
        st.error('❌ Could not connect to the FastAPI server. Make sure it\'s running.')


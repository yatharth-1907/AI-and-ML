from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st 
from langchain_core.prompts import PromptTemplate,load_prompt

load_dotenv()

model= GoogleGenerativeAI(model='gemini-3-flash-preview')

st.header('Research Tools')

paper_input= st.selectbox("Select Research paper Name",["Attension Is All You Need","BERT:Pre-training of Deep Bidirectional Transformers","GPT-3: Language Models are Few short learners","Diffusion Models Beat GANs on Image Synthesis"])
style_input= st.selectbox("Select Explaination style",["Beginner-Friendly","Technical","Code-Oriented","mathematical"])
length_input = st.selectbox("Select the length of the explaination",["Short(1-2 paragraphs)","Medium (3-4 paragraphs)","Long (4-5 paragraphs)"])

template= load_prompt("template.json")

if st.button("Summarize"):
    chain=template | model
    result= chain.invoke({
        'paper_input':paper_input,
        'style_input': style_input,
        "length_input":length_input
    })
    st.write(result)
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

model= ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_Model"))
result= model.invoke("what is the capital of India?")

print(result.content[0]['text'])
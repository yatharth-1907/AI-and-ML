from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model= ChatGoogleGenerativeAI(model="gemini-3-flash-preview")

template1= PromptTemplate(
    template="Write a detailed report on the {topic}",
    input_variables=['topic']
)

template2= PromptTemplate(
    template='write a 5 line summary on the following text \n {text}',
    input_variables=['text']
)
topic= input("Enter the topic for report: ")
# this 4 lines were without parser 
# prompt1= template1.invoke({'topic': topic})

# result= model.invoke(prompt1)

# prompt2= template2.invoke({'text':result.content})

# result= model.invoke(prompt2)

parser= StrOutputParser()

chain= template1 | model | parser | template2 | model | parser

result = chain.invoke({"topic": topic})

print(result)


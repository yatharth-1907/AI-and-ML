from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt1= PromptTemplate(
    template="Generate a detailed report on the {topic}",
    input_variables=['topic']
)

prompt2= PromptTemplate(
    template="Generate a short summary having important 5 points of the following text report \n {text}",
    input_variables=['text']
)

model= ChatGoogleGenerativeAI(model='gemini-3-flash-preview')

parser= StrOutputParser()

chain= prompt1 | model | parser | prompt2 | model | parser

result= chain.invoke("Students not getting job after college.")

print(result)

chain.get_graph().print_ascii()
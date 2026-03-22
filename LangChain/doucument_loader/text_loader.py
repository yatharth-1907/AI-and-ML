from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

model= ChatGoogleGenerativeAI(model='gemini-3-flash-preview')

prompt=PromptTemplate(
    template="Write a summary for the follwing poem -n{poem}",
    input_variables= ['poem']
)

parser= StrOutputParser()

loader= TextLoader(str(Path(__file__).parent/'cricket.txt'),encoding='utf-8')

docs= loader.load()

print(type(docs))

print(len(docs))

print(docs[0].page_content)
print(docs[0].metadata)

chain= prompt | model | parser

print(chain.invoke({'poem':docs[0].page_content}))


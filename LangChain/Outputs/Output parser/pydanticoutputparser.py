from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field

load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3.5-397B-A17B",
    task='text-genration'
)

model= ChatHuggingFace(llm=llm)

class person(BaseModel):
    name: str=Field(description="Name of the person"),
    age: int=Field(description="Age of the person"),
    city: str=Field(description="City in which this person live")

parser= PydanticOutputParser(pydantic_object=person)
    
template= PromptTemplate(
    template='generate the name, age, city of a friction {type} peron \n {format_instruction}',
    input_variables=['type'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)
type= input("Enter the Origin of the person: ")
# prompt= template.invoke({'type':type})
# result= model.invoke(prompt)

chain= template | model | parser
result= chain.invoke({'type':type})
print(result)
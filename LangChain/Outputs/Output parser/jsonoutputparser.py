# cannot define schema of the output.
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os

load_dotenv()

llm= HuggingFaceEndpoint(
    repo_id= "Qwen/Qwen3.5-397B-A17B",
    task="text-generation",
    huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
)

model= ChatHuggingFace(llm=llm)

parser= JsonOutputParser()

template= PromptTemplate(
    template = 'give me 5 facts about {topic} \n {format_instruction}',
    input_variables= ['topic'],
    partial_variables= {'format_instruction': parser.get_format_instructions()}
)

topic= input("Enter the topic: ")
# without chain 
# prompt = template.invoke({'topic':topic})
# result = model.invoke(prompt)
# print(result.content[0]['text'])

chain =  template|model|parser

result= chain.invoke({'topic':topic})

print(result)
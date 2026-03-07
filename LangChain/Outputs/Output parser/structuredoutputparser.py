from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.prompts import PromptTemplate 
import os
# In langchain output_parser is missing.
# from langchain.output_parsers import StructuredOutputParser
from dotenv import load_dotenv

load_dotenv()

llm= HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3.5-397B-A17B",
    task= 'text-generation',
    huggingfacehub_api_token=os.environ['HUGGINGCEFACEHUB_API_TOKEN']
)

model= ChatHuggingFace(llm=llm)


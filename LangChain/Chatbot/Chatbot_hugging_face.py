from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

llm= HuggingFaceEndpoint(
    repo_id= "Qwen/Qwen3.5-397B-A17B",
    task="text-generation",
    huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
)
model= ChatHuggingFace(llm=llm)

result=model.invoke("what is the capital of india")

print(result.content)
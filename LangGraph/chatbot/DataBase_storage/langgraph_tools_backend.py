from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_groq import ChatGroq
from langchain_openrouter import ChatOpenRouter
import os 
# import operator
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient    
from langfuse import observe

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import requests
import random

load_dotenv()

client = MongoClient("mongodb://localhost:27017/")

llm = ChatGroq(model="llama-3.3-70b-versatile")
# llm = ChatOpenRouter(model='minimax/minimax-m2.5:free')

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    
#################################tools####################################

search_tool = DuckDuckGoSearchRun(region='us-en')

@tool
def calculator(first_num: float, second_num,operation: str)->dict:
    '''bPerform a basic arithmetic operation on two numbers.
    Supported operations: add, subtract multipy, divide
    '''
    try :
        if operation == 'add':
            result= first_num + second_num
        elif operation == 'subtract':
            result= first_num - second_num   
        elif operation == 'multiply':
            result= first_num * second_num
        elif operation == 'divide':
            if second_num == 0:
                return {'error': 'Division by zero is not allowed'}
            result= first_num / second_num
        else:
            return {"error":f'''Unsupported operation '{operation}'. '''}
        
        return {'first_num':first_num,'second_num':second_num,'operation':operation,'result':result}
    except Exception as e:
        return {'error': str(e)}
    
@tool
def get_stock_price(symbol:str)-> dict:
    '''Fetch latest stock price for a given symbol (e.g. 'APPLE','TSLA)
    '''
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey=M85VVHL2AWBPYCBW"
    r=requests.get(url)
    return r.json()

############################ Graph Node ####################

#make tool list
tools= [get_stock_price,search_tool,calculator]

#Make the LLM tool-aware
llm_with_tools= llm.bind_tools(tools)
    
@observe(name='Chat_node', as_type='generation')
def chat_node(state: ChatState):
    #take user query from state to LLm and store the response
    messages = state['messages']
    response= llm.invoke(messages)
    return {'messages':[response]}

tool_node = ToolNode(tools) #execute tool call

##################################checkpoint####################################
checkpointer = MongoDBSaver(client)

#Graph Creation
graph= StateGraph(ChatState)

graph.add_node('chat_node',chat_node)
graph.add_node('tools',tool_node)
    
graph.add_edge(START, 'chat_node')
graph.add_conditional_edges('chat_node',tools_condition)
graph.add_edge('tools','chat_node')


chatbot= graph.compile(checkpointer= checkpointer)

def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)

# thread_id='1'
# config={'configurable':{'thread_id': thread_id}}

# for message_chunk,metadata in chatbot.stream(
#     {'messages':[HumanMessage(content='what is the recipe to make maggi')]},
#     config=config,
#     stream_mode='messages'
# ):
#     if message_chunk.content:
#         print(message_chunk.content,end='',flush=True)
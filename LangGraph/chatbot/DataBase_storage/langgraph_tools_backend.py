from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
# from langchain_groq import ChatGroq
# from langchain_openrouter import ChatOpenRouter
from langchain_google_genai import ChatGoogleGenerativeAI

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

# llm = ChatGroq(model="mixtral-8x7b-32768", disable_streaming=True)
# llm = ChatOpenRouter(model='minimax/minimax-m2.5:free')
llm = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash')
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    
#################################tools####################################

_ddg = DuckDuckGoSearchRun(region='us-en')

@tool
def web_search(query: str) -> str:
    """Search the web for current information using DuckDuckGo. 
    Use this for recent events, stock prices, news, or anything requiring up-to-date info.
    
    Args:
        query: The search query string
    """
    return _ddg.invoke(query)

@tool
def calculator(first_num: float, second_num:float ,operation: str)->dict:
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
tools= [get_stock_price,web_search,calculator]

#Make the LLM tool-aware
llm_with_tools= llm.bind_tools(tools)
    
@observe(name='Chat_node', as_type='generation')
def chat_node(state: ChatState):
    #take user query from state to LLm and store the response
    messages = state['messages']
    response= llm_with_tools.invoke(messages)
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


if __name__ == "__main__":
    config = {'configurable': {'thread_id': 'test-123'}}
    
    result = chatbot.invoke(
        {'messages': [HumanMessage(content='who is the parent company of youtube')]},
        config=config
    )
    print(result['messages'][-1].content) 
# thread_id='1'
# config={'configurable':{'thread_id': thread_id}}

# for message_chunk,metadata in chatbot.stream(
#     {'messages':[HumanMessage(content='what is the recipe to make maggi')]},
#     config=config,
#     stream_mode='messages'
# ):
#     if message_chunk.content:
#         print(message_chunk.content,end='',flush=True)
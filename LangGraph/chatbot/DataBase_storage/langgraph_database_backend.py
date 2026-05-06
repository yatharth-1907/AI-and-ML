from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_groq import ChatGroq
# import operator
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient    
from langfuse import observe

load_dotenv()

client = MongoClient("mongodb://localhost:27017/")

llm = ChatGroq(model="llama-3.3-70b-versatile")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    
@observe(name='Chat_node', as_type='generation')
def chat_node(state: ChatState):
    #take user query from state to LLm and store the response
    messages = state['messages']
    response= llm.invoke(messages)
    return {'messages':[response]}
#checkpoint
checkpointer = MongoDBSaver(client)

#Graph Creation
graph= StateGraph(ChatState)

graph.add_node('chat_node',chat_node)
    
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node',END)

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
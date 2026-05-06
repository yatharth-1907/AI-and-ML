from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_groq import ChatGroq
# import operator
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    
def chat_node(state: ChatState):
    #take user query from state to LLm and store the response
    messages = state['messages']
    response= llm.invoke(messages)
    return {'messages':[response]}
#checkpoint
checkpointer = MemorySaver()

#Graph Creation
graph= StateGraph(ChatState)

graph.add_node('chat_node',chat_node)
    
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node',END)

chatbot= graph.compile(checkpointer= checkpointer)

# def convo_name( messages):
#     llm= ChatGroq(model= 'openai/gpt-oss-120b')
#     prompt= f'''You are an AI assistant which give a 20 character tittle to the conversation and the title should be relevent to the conversation: \n
#     {messages}'''
#     title= llm.invoke(prompt).content
#     return title
    

# thread_id='1'
# config={'configurable':{'thread_id': thread_id}}

# for message_chunk,metadata in chatbot.stream(
#     {'messages':[HumanMessage(content='what is the recipe to make maggi')]},
#     config=config,
#     stream_mode='messages'
# ):
#     if message_chunk.content:
#         print(message_chunk.content,end='',flush=True)

import streamlit as st
from langgraph_tools_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

#**************************Utility function *************************
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]
    
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
        
def load_conversation(thread_id):
    return chatbot.get_state(config= {'configurable':{'thread_id':thread_id}}).values['messages']

# ************************** Session SetUp ****************************
#session_state -> dict
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]
    
if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()
    
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()
    
add_thread(st.session_state['thread_id'])
    
# ****************************Sidebar UI ******************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        messages=load_conversation(thread_id)
        
        temp_messages = []
        
        for message in messages:
            if isinstance(message,HumanMessage):
               role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'content':message.content})
        st.session_state['message_history']= temp_messages

#*************************** Main UI **********************************
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input=st.chat_input('Type Here')

if user_input:
    
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
        
    CONFIG={'configurable':{'thread_id': st.session_state['thread_id']}}
        
    # streamlit_DB_frontend.py

    with st.chat_message('assistant'):
        def response_generator():
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            ):
                if metadata.get('langgraph_node') != 'chat_node':
                    continue
                
                content = message_chunk.content
                
                if not content:
                    continue
                
                # Plain string (Groq, OpenAI style)
                if isinstance(content, str):
                    yield content
                
                # List of blocks (Gemini style)
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get('type') == 'text':
                            yield block['text']

        ai_message = st.write_stream(response_generator())
    
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
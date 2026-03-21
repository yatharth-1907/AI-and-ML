from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

prompt1= PromptTemplate(
    template='Generate a redit post about the {topic}',
    input_variables=['topic']
)

prompt2= PromptTemplate(
    template='Generate a linkedin post about the {topic}',
    input_variables=['topic']
)

model= ChatGoogleGenerativeAI(model='gemini-3-flash-preview')

parser= StrOutputParser()

parallel_chain= RunnableParallel({
    'redit': prompt1| model| parser ,
    'linkedin': prompt2| model | parser 
})

result= parallel_chain.invoke("how to win hackathons")

print('Redit')
print(result['redit'])
print()
print()
print("LinkedIn")
print(result['linkedin'])

parallel_chain.get_graph().print_ascii()
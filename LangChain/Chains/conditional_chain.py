from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableParallel, RunnableSequence,RunnableLambda
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

model= ChatGoogleGenerativeAI(model='gemini-3-flash-preview')

parser=StrOutputParser()

class Feedback(BaseModel):
    sentiment: Literal['positive','negative']= Field(description="Give the sentiment of the feedback.")
    
parser2= PydanticOutputParser(pydantic_object=Feedback)

prompt1= PromptTemplate(
    template="Classify the sentiment text feedback into positive or negative \n {feedback} \n {format_instruction}",
    input_variables=['feedback'],
    partial_variables={'format_instruction': parser2.get_format_instructions()}
)

classifier_chain= prompt1| model | parser2

prompt2 = PromptTemplate(
    template="Write a appropriate responce to this positive feedback \n {feedback}",
    input_variables=['feedback']
)

prompt3=PromptTemplate(
    template=" Write an appropriate response to the given negative feedback which should be polite and should reflect that we respect there feedback the will improve and make their experience better \n {feedback}",
    input_variables=['feedback']
)

enrich_input = RunnableParallel({
    "feedback": RunnableLambda(lambda x: x["feedback"]),
    "classification": classifier_chain,
})

branch_chain = RunnableBranch(
    (lambda x: x['classification'].sentiment == 'positive', prompt2|model|parser),
    (lambda x: x['classification'].sentiment == 'negative', prompt3|model|parser),
    RunnableLambda(lambda x: "could not find sentiment")
)

chain= enrich_input | branch_chain

user_feedback = input("Enter your feedback: ").strip()

if not user_feedback:
    user_feedback = "This Phone is good,and best option in this price range."

result= chain.invoke({'feedback': user_feedback})

print(result)

chain.get_graph().print_ascii()

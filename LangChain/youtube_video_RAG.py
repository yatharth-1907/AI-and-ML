from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openrouter import ChatOpenRouter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel, RunnablePassthrough,RunnableLambda
from dotenv import load_dotenv
import os

os.environ['HF_HOME']='D:/huggingface_cache'



load_dotenv()


video_id = "Gfr50f6ZBvo"
youtube_transcript_api = YouTubeTranscriptApi()

try:
    # In recent versions, fetch() returns a FetchedTranscript with snippets.
    fetched_transcript = youtube_transcript_api.fetch(video_id)
    transcript = " ".join([snippet.text for snippet in fetched_transcript.snippets])
    # print(fetched_transcript)
    
except Exception as e:
    print("An error occured while fetching the transcript.")
    print(f"an error occured: {e}")
    

splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks= splitter.create_documents([transcript])

# print(f"Number of chunks: {len(chunks)}")

embeddings= HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore= FAISS.from_documents(chunks,embeddings)

# print(vectorstore.index_to_docstore_id)

retriever= vectorstore.as_retriever(search_type='similarity',search_kwargs= {'k': 4})

# print(retriever.invoke("what is deepmind?"))
def format_docs(retrieved_docs):
    context_text="\n\n".join(doc.page_content for doc in retrieved_docs)
    return  context_text

parser= StrOutputParser()

# llm= ChatOpenRouter(model= "google/gemma-4-31b-it", temperature=0.2)




llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
prompt= PromptTemplate(
    template= """You are a helpful assistant for answering questions about the content of the Youtube video with the following transcript: {context}
    Question: {question}""",
    input_variables=['contxt','question']    
)

parallel_chain= RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
})

# print(parallel_chain.invoke("what is deepminds"))

main_chain= parallel_chain | prompt | llm | parser
question= input('Enter your question: ')
print(main_chain.invoke(question))

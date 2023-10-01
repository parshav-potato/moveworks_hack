import bardapi
import os
from langchain.document_loaders import TextLoader
from langchain.document_loaders.base import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.llms import OpenLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.embeddings import CohereEmbeddings
from dotenv import load_dotenv
from decouple import config


def get_answer(input_text):

    os.environ["COHERE_API_KEY"] = config("COHERE_API_KEY")    
    token = config('TOKEN')
    embeddings = CohereEmbeddings()

    db = FAISS.load_local("new_cohere_index", embeddings)

    context = db.similarity_search(input_text)

    context_str = ""

    for i in context:
        print(i)
        context_str = context_str + i.page_content

    temp_prompt = f"You are a chatbot made to answer user queries for the company Moveworks. Your job is to answer questions based on the context provided. All your knowledge only comes from the context given below. If you don't know the answer to a question just say, I don't know. Never give an answer you are not sure about. Give the output with proper formating.\n Context: %s" %(context_str)
    question_prompt = f"\n Question: %s \n Answer: " %(input_text)
    final_prompt = temp_prompt + question_prompt

    print(final_prompt)
    # Send an API request and get a response.
    answer = bardapi.core.Bard(token).get_answer(final_prompt)
    final_ans = answer['content']

    return final_ans
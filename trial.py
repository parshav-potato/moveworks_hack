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


def get_answer(input_text):

    cohere_api_key = "4DdonhZUMBNF33FX2f65BN6TH1N1jZUYfgfoN7cZ"

    embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key)

    db = FAISS.load_local("cohere_index", embeddings)


    # template = "Using the given context, answer the given question. If you do not know the answer, say I don't know. \n Context: {context} \n Question: {question} \n Answer:?"



    # set your __Secure-1PSID value to key
    token = 'bgi-CgC1Hlbw1u88K-CdGKdqHa84_qRJ9wqqyFwKklcBXQNZT2__Z-DzXXVVT3FHp8KtLg.'

    # set your input text
    # input_text = "Can you tell me about the article on how to unlock continual service improvement with AIOps?"


    context = db.similarity_search(input_text)


    context_str = ""

    for i in context:
        print(i)
        context_str = context_str + i.page_content
    # prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    temp_prompt = f"Only use the following context to answer the question. If you do not know the answer of the the question say I don't know. \n Context: %s" %(context_str)
    question_prompt = f"\n Question: %s \n Answer: " %(input_text)
    final_prompt = temp_prompt + question_prompt

    print(final_prompt)
    # Send an API request and get a response.
    answer = bardapi.core.Bard(token).get_answer(final_prompt)
    final_ans = answer['content']

    return final_ans
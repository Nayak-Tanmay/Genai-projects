from dotenv import load_dotenv
import os
import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Answer the question accordingly."),
    ("user", "Question: {question}")
])

st.title("Chatbot using gemma model")
text_input = st.text_input("What do you have in your mind?")

llm = Ollama(model="gemma:2b")
parser = StrOutputParser()
chain = prompt | llm | parser

if text_input:
    st.write(chain.invoke({"question": text_input}))









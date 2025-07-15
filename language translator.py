import sys
import streamlit as st


st.write("Python executable:", sys.executable)

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

groq_api_key=os.getenv("GROQ_API_KEY")
llm=ChatGroq(groq_api_key=groq_api_key,model="Gemma2-9b-It")

parser=StrOutputParser()

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","Convert the text into following {language}"),
        ("user","{text}")
    ]
)
chain=prompt|llm|parser

st.title("Langchain language translator")
language=st.text_input("Enter your desired language")
text=st.text_input("Enter the text you want to convert")

if language and text:
    st.write(chain.invoke({"language":language,"text":text}))





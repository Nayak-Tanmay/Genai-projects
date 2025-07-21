import os
from dotenv import load_dotenv
load_dotenv()

import validators

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

st.set_page_config(page_title="Langchain:Summarize Text from YT or website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize URL")

with st.sidebar:
    groq_api_key=st.text_input("Groq api key",value="",type='password')

generic_url=st.text_input("Generic URL",label_visibility='collapsed')

llm=ChatGroq(model="llama-3.1-8b-instant",groq_api_key=groq_api_key)

generic_template="""
Summarize the following in under 300 words
Text:{text}

"""

prompt=PromptTemplate(input_variables=["text"],template=generic_template)

if st.button("Summarize content from YT or Website"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid Url. It can may be a YT video utl or website url")
    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the website or yt video data
                if "youtube.com" in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs=loader.load()

                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception:{e}")
            



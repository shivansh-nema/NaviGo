import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI

ai_api_key = st.secrets["AI_API_KEY"]
headers = {
    "authorization": ai_api_key,
    "content-type": "application/json"
}
model_name = "gemini-2.0-flash"
project_id = "323423126135" 

st.set_page_config(
    page_title="NaviGo",
    page_icon="Navigo_Icon.png",
)

page_bg_img = """
<style>
.block-container {
        padding-top: 3rem !important;
}
# header { visibility: hidden; }

[data-testid="stAppViewContainer"]{
    background-image: url(https://images.unsplash.com/photo-1551309292-e185c0b6e22a?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D);
    background-size: cover;
}

[data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
}

[data-testid="stSidebarContent"]{
    background-image: url(https://images.unsplash.com/photo-1669295384050-a1d4357bd1d7?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D);
    background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("AI Travel Assistant")

pdf_Reader = PdfReader("Detailed_Travel_Essentials_Guide.pdf")
text = ""
for page in pdf_Reader.pages:
    text += page.extract_text()

text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
chunks = text_splitter.split_text(text)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=ai_api_key)

vector_store = FAISS.from_texts(chunks, embeddings)

user_question = st.text_input("Type your question here :-   ")

if user_question:
    match = vector_store.similarity_search(user_question)

    llm = ChatGoogleGenerativeAI(
        api_key=ai_api_key,
        temperature=1,
        max_tokens=1000,
        model= model_name,
        project= project_id
    )

    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=match, question=user_question)
    st.write(response)

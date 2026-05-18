import streamlit as st
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI 旅平險專員", page_icon="🛡️", layout="wide")
st.title("🛡️ AI 旅平險專員")
st.caption("國泰・富邦・新光 三家旅平險保單 RAG 智慧問答系統 | 生成式 AI 期末報告")

@st.cache_resource
def load_vectorstore():
    index_path = "faiss_index"
    if os.path.exists(index_path):
        return FAISS.load_local(index_path, HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"), allow_dangerous_deserialization=True)
    
    st.info("首次執行，正在解析 3 份 PDF 並建立向量資料庫...")
    loader = PyPDFDirectoryLoader("data/")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local(index_path)
    st.success(f"✅ 已處理 {len(splits)} 個文件區塊！")
    return vectorstore

vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("例如：班機延誤多久可以理賠？酒醉受傷是否理賠？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("正在查詢保單條文..."):
            result = qa_chain.invoke({"query": prompt})
            answer = result["result"]
            st.markdown(answer)
            
            st.caption("📌 引用條文：")
            for doc in result.get("source_documents", []):
                source = doc.metadata.get("source", "保單").split("/")[-1]
                st.markdown(f"- **{source}**：{doc.page_content[:180]}...")

    st.session_state.messages.append({"role": "assistant", "content": answer})

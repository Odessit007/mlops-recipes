import os
from typing import Literal

from dotenv import load_dotenv
from langchain import hub
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from PyPDF2 import PdfReader
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import torch


torch.classes.__path__ = []  # See "Issue with torch.classes" section in README


def main():
    load_dotenv()
    print(os.environ["GEMINI_API_KEY"])
    st.set_page_config(page_title="Chat with PDF")
    st.header("Chat with PDF")

    # Upload PDF
    pdf = st.file_uploader("Upload PDF", type="pdf")

    # Read PDF
    if pdf is not None:
        print(pdf)
        text = read_pdf(pdf)
        chunks = split_text(text)
        embeddings = get_embeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        question = st.text_input("Ask a question:")
        if question:
            documents = knowledge_base.similarity_search(question)
            st.write(documents)
            model_name = os.environ["GEMINI_CHAT_MODEL"]
            llm = GoogleGenerativeAI(model=model_name)

            # Define prompt for question-answering
            prompt = hub.pull("rlm/rag-prompt")
            # prompt = ChatPromptTemplate.from_template("Summarize this content: {context}")
            docs_content = "\n\n".join(doc.page_content for doc in documents)
            messages = prompt.invoke({"question": question, "context": docs_content})
            response = llm.invoke(messages)
            # chain = create_stuff_documents_chain(llm, prompt)
            # result = chain.invoke({"context": documents})
            st.write(response)


def read_pdf(pdf: UploadedFile) -> str:
    pdf_reader = PdfReader(pdf)
    return "".join(page.extract_text() for page in pdf_reader.pages)


def split_text(text: str) -> list[str]:
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
    )
    return text_splitter.split_text(text)


def get_embeddings(mode: Literal["google", "local"] = "google") -> Embeddings:
    if mode == "local":
        model_name = os.environ["HUGGINGFACE_EMBEDDING_MODEL"]
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}  # This is because
        )
    model_name = os.environ["GEMINI_EMBEDDING_MODEL"]
    return GoogleGenerativeAIEmbeddings(model=model_name)


if __name__ == "__main__":
    main()

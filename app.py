#import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import pickle
from pathlib import Path
from langchain_community.vectorstores.faiss import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_docs(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    # Save the vector store locally
    vector_store.save_local("faiss-index")
    print(f"FAISS index saved in directory '{faiss-index}'.")


def get_conversational_chain():
    prompt_template = """
   Read the document answer the questions related to the provided context. \
    If the information asked is not mentioned accurately simply answer "I dont know the answer of this question and avoid giving wrong Answer, Context::\n {context}\n , question \n {question}\n Answer:

    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=1)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain
#
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.load_local(Path("faiss-index"), embeddings, allow_dangerous_deserialization=True)
    docs = vector_store.similarity_search(user_question)
    chain = get_conversational_chain()

    response = chain.invoke(
        {"input_documents": docs, "question": user_question}
    )
    print("Reply:", response["output_text"])

if __name__ == "__main__":
    user_question = input("Enter your question: ")
    user_input(user_question)

# Testing the functions
# if __name__ == "__main__":
#     # List of PDF documents to be processed (replace with your actual PDF file paths)
#     pdf_docs = ["AkinsolaJET-IJCTT-V48P126.pdf", "ART20203995.pdf"]
#
#     # Step 1: Extract text from PDF documents
#     extracted_text = get_pdf_docs(pdf_docs)
#     print("Extracted text:", extracted_text[:500])  # Print the first 500 characters of the extracted text for verification
#
#     # Step 2: Split the extracted text into chunks
#     text_chunks = get_text_chunks(extracted_text)
#     print(f"Number of text chunks: {len(text_chunks)}")
#     print("First chunk:", text_chunks[0])  # Print the first chunk for verification
#
#     # Step 3: Create a vector store from text chunks and save it locally
#     vector_store = get_vector_store(text_chunks)
#     print("Vector store created and saved.")
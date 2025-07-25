# -*- coding: utf-8 -*-
"""RAG-based QA Bot for Research Insights

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j92yidZZVEJ8LpN8GhLvSHmcBtePBqyZ
"""



pip install -U langchain-community

pip install pypdf

from langchain_community.document_loaders import PyPDFLoader

pdf_path = "/content/sample_research_paper.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

print("Loaded Document Sample:\n")
print(documents[0].page_content[:500])

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("sample_research_paper.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

split_docs = text_splitter.split_documents(documents)

print(f"Number of chunks: {len(split_docs)}")
print("Sample chunk:\n")
print(split_docs[0].page_content)

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("sample_research_paper.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(documents)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

sample_texts = [doc.page_content for doc in split_docs[:2]]
embeddings = embedding_model.embed_documents(sample_texts)

print(f"Number of embeddings: {len(embeddings)}")
print(f"Length of each embedding vector: {len(embeddings[0])}")

pip install chromadb

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("sample_research_paper.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(documents)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_db = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding_model,
    persist_directory="./chroma_db"
)
vector_db.persist()

print("Chroma vector database created and stored at './chroma_db'")

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)

retriever = vector_db.as_retriever(search_kwargs={"k": 2})

query = "What is this paper about?"
results = retriever.get_relevant_documents(query)

print("Top matching chunks:\n")
for i, doc in enumerate(results, start=1):
    print(f"Chunk {i}:\n{doc.page_content[:300]}\n{'-'*40}")

from transformers import pipeline
from langchain.llms import HuggingFacePipeline

# Load public LLM pipeline
llm_pipeline = pipeline(
    "text-generation",
    model="tiiuae/falcon-7b-instruct",
    max_new_tokens=500,
    temperature=0.7
)

llm = HuggingFacePipeline(pipeline=llm_pipeline)


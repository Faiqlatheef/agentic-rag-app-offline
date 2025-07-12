from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import (
    TextLoader, PDFPlumberLoader, Docx2txtLoader, UnstructuredExcelLoader, CSVLoader
)
from .base_agent import BaseAgent
from .utils import configure_logging, safe_read_file
from config.settings import settings
from loguru import logger
import os
import tempfile

configure_logging()

class RAGAgent(BaseAgent):
    def __init__(self):
        logger.info("Initializing Local RAG Agent...")
        self.vectorstore = None
        self.qa_chain = None
        self.base_llm = ChatOllama(model=settings.LLM_MODEL)
        self._build_vectorstore_from_file(settings.DOCUMENT_PATH)

    def _build_vectorstore_from_documents(self, documents):
        embed = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = FAISS.from_documents(documents, embed)
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": settings.TOP_K})
        llm = ChatOllama(model=settings.LLM_MODEL)
        self.qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    def _build_vectorstore_from_file(self, path):
        raw = safe_read_file(path)
        splitter = CharacterTextSplitter(chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
        chunks = splitter.split_text(raw)
        documents = [Document(page_content=c) for c in chunks]
        self._build_vectorstore_from_documents(documents)

    def run(self, query: str) -> str:
        if not query.strip():
            return "Please enter a question."

        try:
            if self.vectorstore is None:
                logger.info("No documents uploaded. Using base LLM.")
                return str(self.base_llm.invoke(query))

            result = self.qa_chain.invoke({"query": query})
            answer = result["result"]
            if "I don't know" in answer or len(answer.strip()) < 10:
                return str(self.base_llm.invoke(query))

            return answer
        except Exception as e:
            logger.error(f"run() error: {e}")
            return "❌ An error occurred."


    def get_context(self, query: str) -> str:
        try:
            docs = self.qa_chain.retriever.invoke(query)
            return "\n\n".join(d.page_content for d in docs)
        except Exception as e:
            logger.error(f"Context retrieval failed: {e}")
            return "No context available."

    def ingest_new_documents(self, file_path):
        try:
            extension = os.path.splitext(file_path)[1].lower()

            if extension == ".pdf":
                from langchain_community.document_loaders import PDFPlumberLoader
                loader = PDFPlumberLoader(file_path)
            elif extension == ".docx":
                from langchain_community.document_loaders import Docx2txtLoader
                loader = Docx2txtLoader(file_path)
            elif extension in [".xls", ".xlsx"]:
                from langchain_community.document_loaders import UnstructuredExcelLoader
                loader = UnstructuredExcelLoader(file_path, mode="elements")
            elif extension == ".csv":
                from langchain_community.document_loaders import CSVLoader
                loader = CSVLoader(file_path=file_path)
            elif extension == ".txt":
                from langchain_community.document_loaders import TextLoader
                loader = TextLoader(file_path, encoding="utf-8")
            else:
                return f"❌ Unsupported file type: {extension}"

            documents = loader.load()
            if not documents:
                return "❌ No documents extracted."

            self._build_vectorstore_from_documents(documents)
            return f"✅ {extension.upper()} file indexed with {len(documents)} chunks."
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return f"❌ Upload error: {e}"


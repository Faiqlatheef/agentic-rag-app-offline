class Settings:
    DOCUMENT_PATH = "data/sample_docs.txt"
    LOG_PATH = "logs/rag_agent.log"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    TOP_K = 3
    LLM_MODEL = "llama3"  # Ollama model name

settings = Settings()

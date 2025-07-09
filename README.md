# Agentic RAG App (Offline / Local Only)

A Retrieval-Augmented Generation (RAG) app that works **without OpenAI** by using:
- `HuggingFaceEmbeddings` for embedding
- `ChatOllama` with LLaMA 3 running via Ollama

## 🚀 How to Run

### 1. Install Ollama
https://ollama.com

```bash
ollama run llama3
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app.py
```

Then go to: http://127.0.0.1:7860

# 📚 Full Documentation: Agentic RAG App (Local, No API Cost)

## 🧠 Overview

The Agentic RAG App is a locally hosted Retrieval-Augmented Generation (RAG) system that allows users to:
- Upload documents (PDF, DOCX, CSV, Excel, TXT)
- Ask questions based on those documents
- Chat freely using a local Large Language Model (LLM) like LLaMA3 via Ollama
- Operate entirely offline, with no OpenAI or external API requirement

---

## 🏗️ Project Structure

```
agentic_rag_app_local/
├── app.py                  # Main application entry point
├── .env                    # Configuration variables (model name, ports)
├── requirements.txt        # Python dependencies
├── README.md               # Project overview
├── DOCUMENTATION.md        # Full documentation (this file)
├── agent/
│   └── rag_agent.py        # Core RAG logic: embedding, vector store, context
├── ui/
│   └── gradio_ui.py        # Gradio UI and user interactions
└── utils/
    └── file_loader.py      # Multi-format document loader
```

---

## ⚙️ Installation & Setup

### 🔧 Prerequisites

- Python 3.10+
- Ollama installed: https://ollama.com/
- Git (optional)
- Virtualenv (recommended)

### 📥 Clone and Install

```bash
git clone https://github.com/Faiqlatheef/agentic-rag-app-offline.git
cd agentic_rag_app_local
pip install -r requirements.txt
```

### 🧠 Run Local LLM

```bash
ollama run llama3
```

### 🚀 Run the App

```bash
python app.py
```

Visit: http://127.0.0.1:7860

---

## 💡 Key Features & Implementation Details

### 1. ✅ Dual Chat Modes

**Gradio UI** has two tabs:
- **Ask from Documents**: Runs RAG-based QA
- **General Chat**: Pure LLM generation (like ChatGPT)

### 2. 🧾 File Upload and Parsing

`file_loader.py` supports:
- PDF → `PyPDFLoader`
- DOCX → `docx.Document`
- TXT → Raw reader
- CSV, XLSX → `pandas.read_csv` and `read_excel`

All documents are chunked and returned as LangChain `Document` objects.

### 3. 🔍 Embeddings + Vector DB

- **Embeddings**: Uses `HuggingFaceEmbeddings("all-MiniLM-L6-v2")`
- **Vector Store**: FAISS (local, fast, no cloud)

On file upload:
- Each doc is embedded
- Stored in vector DB for retrieval

### 4. 🧠 RAG Logic in `rag_agent.py`

```python
retriever = self.vectorstore.as_retriever()
llm = ChatOllama(model=settings.LLM_MODEL)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
```

On query:
- Retrieve top k docs
- Combine with LLM response
- Append context + formatted answer

### 5. 🗂️ UI in `gradio_ui.py`

#### Two Chatbots:

```python
doc_chatbox = gr.Chatbot(label="Document Chat History", type="messages")
free_chatbox = gr.Chatbot(label="General Chat History", type="messages")
```

#### Button Handlers:

```python
btn_doc_chat.click(...)         # Uses RAG agent
btn_free_chat.click(...)        # Uses LLM directly
upload_button.upload(...)       # Triggers file loader + embed pipeline
```

### 6. 🧵 Conversation Format (Gradio >= 4)

Switched from `(question, answer)` tuples to:
```python
{"role": "user", "content": "..."}
{"role": "assistant", "content": "..."}
```

### 7. ⚙️ Env Configuration

`.env` file:

```dotenv
LLM_MODEL=llama3
VECTOR_DB_PATH=vector_store/
EMBED_MODEL=all-MiniLM-L6-v2
```

---

## 🧪 Testing the System

1. Upload a `.pdf` or `.docx` file
2. Ask: _"What is this document about?"_ or _"Summarize key points"_
3. Switch tab and ask: _"What is LLMOps?"_

---

## 📁 Supported Formats

| Format | Notes |
|--------|-------|
| `.pdf` | Multi-page supported |
| `.docx` | With or without formatting |
| `.csv` | Tabular data QA |
| `.xlsx` | Multi-sheet Excel |
| `.txt` | Raw text or log files |

---

## 🛠️ Troubleshooting

| Issue | Fix |
|-------|-----|
| Chatbot error: tuple format | Use `type="messages"` and dict format |
| Ollama LLM doesn't start | Ensure `ollama run llama3` is active |
| PDF not parsing | Check if scanned image-only PDFs |
| Vector store not updating | Clear old FAISS index or force reload |

---

## 🛠️ Future Ideas

- Streamed LLM responses
- Chat memory/history persistence
- Hybrid search (vector + keyword)
- Multi-file Q&A summarization
- Named entity linking in answers

---

## 📄 License

MIT License. Open for modification and commercial/non-commercial use.

---

## 🙋‍♀️ Author & Contributions

Built by Abdul Latheef Faiq Ahamed ✨  
Feel free to contribute, fork, or open PRs!

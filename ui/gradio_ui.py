import gradio as gr
from agent.rag_agent import RAGAgent
from loguru import logger

class RAGUI:
    def __init__(self):
        self.agent = RAGAgent()
        self.doc_chat_history = []
        self.free_chat_history = []

    def handle_query_with_context(self, user_input):
        if not user_input.strip():
            return "Type your question", self.doc_chat_history

        answer = str(self.agent.run(user_input))
        context = str(self.agent.get_context(user_input))

        full_answer = f"📌 Answer: \n{answer}\n\n🧾 Context Retrieved: \n{context}"

        self.doc_chat_history.append({"role": "user", "content": user_input})
        self.doc_chat_history.append({"role": "assistant", "content": full_answer})

        return full_answer, self.doc_chat_history


    def handle_query_freely(self, user_input):
        if not user_input.strip():
            return "Type your question", self.free_chat_history

        response = self.agent.base_llm.invoke(user_input)
        answer = response.content if hasattr(response, "content") else str(response)

        self.free_chat_history.append({"role": "user", "content": user_input})
        self.free_chat_history.append({"role": "assistant", "content": answer})

        return answer, self.free_chat_history


    def handle_upload(self, file_path):
        return self.agent.ingest_new_documents(file_path)

    def launch(self):
        with gr.Blocks() as ui:
            gr.Markdown("## 🧠 Agentic RAG App: Document QA + General Chat")

            with gr.Tab("📁 Upload & Ask from Document"):
                with gr.Row():
                    file_input = gr.File(label="Upload Document (PDF, DOCX, XLSX, CSV, TXT)", type="filepath")
                    upload_status = gr.Textbox(label="Upload Status")
                    upload_button = gr.Button("Upload")
                    upload_button.click(self.handle_upload, inputs=file_input, outputs=upload_status)

                doc_question = gr.Textbox(label="Ask a Question (with Document Context)", lines=2)
                doc_submit = gr.Button("Submit Document Query")
                doc_answer = gr.Textbox(label="Answer + Context", lines=8)
                doc_chatbox = gr.Chatbot(label="Document Chat History", type="messages")
                doc_submit.click(self.handle_query_with_context, inputs=doc_question, outputs=[doc_answer, doc_chatbox])

            with gr.Tab("💬 Chat Freely"):
                free_question = gr.Textbox(label="Ask Anything (No Context)", lines=2)
                free_submit = gr.Button("Submit Free Chat")
                free_answer = gr.Textbox(label="Response", lines=8)
                free_chatbox = gr.Chatbot(label="General Chat History", type="messages")
                free_submit.click(self.handle_query_freely, inputs=free_question, outputs=[free_answer, free_chatbox])


        ui.launch()

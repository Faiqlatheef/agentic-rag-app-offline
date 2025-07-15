from ui.gradio_ui import RAGUI
from loguru import logger

if __name__ == "__main__":
    logger.info("Launching Local RAG App...")
    print("✅ RAG App started...\nIf the link appears below, press Ctrl and click on the link http://127.0.0.1:7860")
    try:
        app = RAGUI()
        app.launch()
    except Exception as e:
        logger.exception("Failed to launch RAG App")
        print("❌ Launch failed:", e)

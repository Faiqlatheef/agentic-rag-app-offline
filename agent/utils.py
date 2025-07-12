from loguru import logger
from config.settings import settings

def configure_logging():
    logger.remove()
    logger.add(settings.LOG_PATH, rotation="1 MB", level="INFO", enqueue=True)
    logger.info("Logger initialized")

def safe_read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return ""

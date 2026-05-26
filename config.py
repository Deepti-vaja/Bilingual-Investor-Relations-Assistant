import os
from pathlib import Path
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Secure Tokens
HF_TOKEN = os.getenv("HF_TOKEN")

# File Paths
DATA_FOLDER = Path("Data")
CHUNK_FILE_EN = Path("chunked_docs_en.pkl")
CHUNK_FILE_JP = Path("chunked_docs_jp.pkl")
FAISS_PATH_EN = Path("vector_db/faiss_index_en")
FAISS_PATH_JP = Path("vector_db/faiss_index_jp")

# Document Processing Settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 150

# Model Names
EMBEDDING_MODEL_NAME = "BAAI/bge-m3"
LLM_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Retriever Settings
SEARCH_K = 3

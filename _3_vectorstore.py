from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import logging

from config import FAISS_PATH_EN, FAISS_PATH_JP, EMBEDDING_MODEL_NAME, SEARCH_K

logger = logging.getLogger(__name__)


def _load_or_create_faiss(
    chunked_docs: list[Document],
    faiss_path: Path,
    embedding_model: HuggingFaceEmbeddings
) -> FAISS:
    """Helper function to load an existing FAISS vectorDB from disk or create it."""
    # Check if index exists locally
    if faiss_path.exists() and (faiss_path / "index.faiss").exists():
        vectorstore = FAISS.load_local(
            str(faiss_path),
            embedding_model,
            allow_dangerous_deserialization=True  # Required by newer FAISS versions
        )
        logger.info(f"Loaded existing vector DB from {faiss_path.name} ✅")
        return vectorstore
    
    # Otherwise, generate from chunks
    logger.info(f"Creating new vector DB at {faiss_path.name}...")
    vectorstore = FAISS.from_documents(chunked_docs, embedding_model)
    vectorstore.save_local(str(faiss_path))
    logger.info(f"Created and saved vector DB at {faiss_path.name} 🆕")
    return vectorstore


def get_vectorstores(chunked_en: list[Document], chunked_jp: list[Document]):
    """
    Initializes embeddings, creates/loads vectorstores, and returns them directly 
    so we can access similarity scores later.
    Returns (vectorstore_en, vectorstore_jp).
    """
    # Initialize shared embedding model directly
    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    vectorstore_en = _load_or_create_faiss(chunked_en, FAISS_PATH_EN, embedding_model)
    vectorstore_jp = _load_or_create_faiss(chunked_jp, FAISS_PATH_JP, embedding_model)

    return vectorstore_en, vectorstore_jp

import pickle
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import logging

from config import CHUNK_FILE_EN, CHUNK_FILE_JP, CHUNK_SIZE, CHUNK_OVERLAP

logger = logging.getLogger(__name__)


def _process_language_chunks(
    documents: list[Document],
    cache_file: Path,
    chunk_size: int,
    chunk_overlap: int
) -> list[Document]:
    """Helper function to load cached chunks or create new ones for a target language."""
    if cache_file.exists():
        with open(cache_file, "rb") as f:
            chunked_docs = pickle.load(f)
        logger.info(f"Loaded {len(chunked_docs)} chunks from file {cache_file.name} ")
        return chunked_docs

    # If no cache, split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunked_docs = []
    for doc in documents:
        chunks = text_splitter.split_documents([doc])
        chunked_docs.extend(chunks)
    
    # Save cache
    with open(cache_file, "wb") as f:
        pickle.dump(chunked_docs, f)
        
    logger.info(f"Created and saved {len(chunked_docs)} chunks to {cache_file.name} ")
    return chunked_docs


def chunk_documents(all_docs: list[Document]) -> tuple[list[Document], list[Document]]:
    """
    Filters documents by language and applies text chunking. Returns (English chunks, Japanese chunks).
    """
    logger.info("Starting chunking process...")
    # Filter documents by language
    en_docs = [doc for doc in all_docs if doc.metadata.get('language') == 'en']
    
    # Note: langdetect often detects Japanese as 'ja' rather than 'jp'
    jp_docs = [doc for doc in all_docs if doc.metadata.get('language') in ['ja', 'jp']]

    chunked_en = _process_language_chunks(en_docs, CHUNK_FILE_EN, CHUNK_SIZE, CHUNK_OVERLAP)
    chunked_jp = _process_language_chunks(jp_docs, CHUNK_FILE_JP, CHUNK_SIZE, CHUNK_OVERLAP)

    return chunked_en, chunked_jp

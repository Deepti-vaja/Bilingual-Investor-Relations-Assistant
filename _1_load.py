import re
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langdetect import detect
import logging

from config import DATA_FOLDER

# Configure lightweight logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """Removes weird characters and normalizes spaces."""
    text = text.replace("\u00ad", "")  # remove soft hyphen
    text = re.sub(r"[ \t]+\n", "\n", text)  # clean spaces before newline
    text = re.sub(r"\n{3,}", "\n\n", text)  # limit newlines
    text = re.sub(r"[ ]{2,}", " ", text)   # normalize spaces
    return text.strip()


def load_and_clean_data(data_dir: Path = DATA_FOLDER) -> list[Document]:
    """
    Loads all PDF documents from the given folder, detects language,
    and cleans text content.
    """
    all_data_documents = []
    
    if not data_dir.exists():
        logger.warning(f"Data directory {data_dir} does not exist. Please create it and add PDFs.")
        return all_data_documents

    for file in data_dir.rglob("*.pdf"):
        try:
            loader = PyMuPDFLoader(file_path=str(file))
            documents = loader.load()
            for doc in documents:
                # Detect language (fallback to generic if detection fails)
                try:
                    lang = detect(doc.page_content)
                except Exception:
                    lang = "en"

                # Wrap page in Document with metadata and cleaned content
                all_data_documents.append(
                    Document(
                        page_content=clean_text(doc.page_content),
                        metadata={
                            "source": str(file),
                            "language": lang  # EN / JA
                        }
                    )
                )
            logger.info(f"Loaded and cleaned {file.name}")
        except Exception as e:
            logger.error(f"Error loading {file}: {e}")

    logger.info(f"Total pages loaded: {len(all_data_documents)}")
    return all_data_documents

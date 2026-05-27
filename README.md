## 📑 Table of Contents

- [Objective](#-objective)
- [Features](#-features)
- [CLI Output](#️-cli-output)
- [Architecture](#️-architecture)
- [Tech Stack](#️-tech-stack)
- [Installation & Setup](#-installation--setup)
- [Author](#-author)
  
## 💡 Example Queries

```text
What was the total revenue?
最も一般的で直接的な聞き方です。？
What are the company growth trends?
```
## 🛠️ Tech Stack

### 🐍 Core Language
- Python

---

### 📄 Document Processing
- **PyMuPDF** – PDF text extraction  
- **RecursiveCharacterTextSplitter** – Text chunking and splitting large documents  

---

### 🧠 Embeddings & Models
- **sentence-transformers** – Multilingual embeddings  
- **BAAI/bge-m3** – Embedding model used for semantic search  
- **TinyLlama/TinyLlama-1.1B-Chat-v1.0** – Lightweight LLM for response generation  

---

### 🌐 Language Handling
- **langdetect** – Detects input language (English / Japanese)  

---

### 📊 Vector Database
- **FAISS** – Fast similarity search and retrieval of document chunks  

---

### 💬 Application Interface
- **CLI-based Chatbot** – Terminal-based interaction system  

---

### 🔐 Environment & Utilities
- **python-dotenv** – Environment variable management  

---

### 📜 Additional Features
- Chat history storage  
- Metadata filtering (document type-based retrieval)  

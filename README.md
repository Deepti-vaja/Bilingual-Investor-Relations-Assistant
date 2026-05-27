#  **🚀 Bilingual Investor Relations Assistant**

## 🎯 Objective

The Bilingual Investor Relations Assistant is an LLM-powered RAG based system designed to analyze and retrieve insights from English and Japanese financial documents using semantic search and context-aware interaction.

## 🎯 Purpose

Exploring financial reports manually can be overwhelming — especially when important insights are scattered across lengthy English and Japanese documents.

The Bilingual Investor Relations Assistant turns this process into a more natural and interactive experience. Instead of relying on traditional keyword searching, users can simply ask questions in their preferred language and receive relevant, context-aware responses generated directly from the documents.

To make retrieval more transparent and trustworthy, the system also surfaces the most relevant document chunks along with similarity scores behind each response. Combined with conversational memory, this creates a smoother and more intuitive way to explore sensitive information.

## Architecture 

```text
Bilingual Investor Relations Assistant
├── src/
│   ├── _1_load.py
│   ├── _2_chunk.py
│   ├── _3_vectorstore.py
│   ├── _4_prompt.py
│   ├── _5_llm.py
│   ├── main.py
│   ├── models.py                        # Defines data models and schemas
│   ├── config.py                          # Central configuration 
│   └── chat_history.py
├── storage/
│      ├── chunked_doc                    # Stores preprocessed document chunks to avoid recomputation 
│      │      ├── chunked_docs_en.pkl
│      │      └── chunked_docs_jp.pkl
│      │
│      └── vector_db/                     # FAISS-based vector databases for semantic retrieval
│             ├── faiss_index_en 
│             │          ├── index.faiss
│             │          └── index.pkl   # metadata mapping
│             │
│             └── faiss_index_jp
│                        ├── index.faiss
│                        └── index.pkl  
│
│ 
├── DATA/                              # (EN / JP  IR Reports)
│   ├── FinancialResults_24Q1_E (7).pdf
│   └── FinancialResults_25Q1_J (7).pdf
│
├── README.md
└── requirements.txt

```

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
  
## ✨ Features

- 🌐 Multilingual query handling (EN / JP)   
- 🔍 Intelligent document retrieval using FAISS vector search  
- ✂️ Automatic document chunking for efficient processing  
- 🏷️ Metadata-aware retrieval for better document filtering  
- 💬 CLI-based conversational chatbot interface  
- 📜 Chat history tracking for conversational context  
- ⚡ Fast similarity search using multilingual embeddings  
- 🤖  LLM-powered answer generation using TinyLlama  
- 📊 Displays retrieved chunks with similarity scores for transparency  
- 🔐 Environment-based configuration using “.env” support  
- 🧩 Modular pipeline architecture for scalability and maintainability  
- 📁 Cached chunk storage to avoid repeated preprocessing  
 

### Phase 1: Data Indexing

```text
  Raw IR Documents             Processing & Chunking                 Vector Isolation
 ┌─────────────────┐        ┌─────────────────────────┐        ┌───────────────────────────┐
 │ DATA/           │ ───>   │ src/_1_load.py          │ ───>   │  src/_3_vectorstore.py    │
 │  • EN Report    │        │ src/_2_chunk.py         │        │                           │
 │  • JP Report    │        └─────────────────────────┘        └───────────────────────────┘
 └─────────────────┘                     │                                   │
                                         ▼                                   ▼
                            
                            storage/chunked_doc/                storage/vector_db/
                            │                                    │
                            ├── chunked_docs_en.pkl             ├── faiss_index_en/
                            └── chunked_docs_jp.pkl             └── faiss_index_jp/
```


### PHASE 2: RETRIEVAL AND GENERATION 
```text
               ┌────────────────────────────────────────────────────────┐
               │                     User Request                       │
               │          "What was the total revenue?" (EN)            │
               └────────────────────────────────────────────────────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │   Language Router   │ (Auto-detects EN vs. JP)
                                └─────────────────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                             ▼
          [ Target: EN Index ]                          [ Target: JP Index ]
         src/_3_vectorstore.py                         src/_3_vectorstore.py
                    │                                             │
                    └──────────────────────┬──────────────────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │ Top-K Context Match │ (Extracts precise financial text)
                                └─────────────────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │ Prompt Construction │ <─── [ chat_history.py ]
                                │   src/_4_prompt.py  │      (Injects context + guardrails)
                                └─────────────────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │    LLM Generation   │
                                │    src/_5_llm.py    │
                                └─────────────────────┘
                                           │
                                           ▼
                                ┌─────────────────────┐
                                │  Grounded Response  │ 
                                └─────────────────────┘

```


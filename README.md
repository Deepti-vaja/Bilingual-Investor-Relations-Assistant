# 🚀 Bilingual Investor Relations Assistant

> Multilingual RAG-based financial document assistant for English and Japanese investor relations reports

![Python](https://img.shields.io/badge/Python-3.10-blue)
![TinyLlama](https://img.shields.io/badge/LLM-TinyLlama-black)
![FAISS](https://img.shields.io/badge/VectorDB-FAISS-teal)
![BGE-M3](https://img.shields.io/badge/Embedding-BGE--M3-green)
![RAG](https://img.shields.io/badge/Architecture-RAG-orange)
![Language](https://img.shields.io/badge/Language-EN%20%7C%20JP-purple)


## 📑 Table of Contents

- [🎯 Overview](#-overview)
- [🏗️ Architecture](#️-architecture)
- [💡 Example Queries](#-example-queries)
- [🖥️ CLI Output](#cli-output)
- [⚙️ How It Works](#️-how-it-works)
- [🛠️ Tech Stack](#️-tech-stack)
- [🧠 Technical Design Decisions](#technical-design-decisions)
- [✨ Features](#features)
- [⚙️ End-to-End Processing Pipeline](#pipeline)
- [🚀 Installation & Setup](#-installation--setup)
- [⚙️ Setup Flow](#️-setup-flow)
- [👩‍💻 Author](#author)

## 🎯 Overview

The Bilingual Investor Relations Assistant is a multilingual RAG-based
system designed to analyze English and Japanese financial documents
through semantic retrieval and context-aware interaction.

Instead of relying on traditional keyword search, users can ask
questions naturally and receive grounded responses generated directly
from investor relations reports.

To improve transparency, the system also displays retrieved document
chunks and similarity scores behind each response.


## 🏗️ Architecture 

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


  
## 💡 Example Queries

```text
What was the total revenue?
最も一般的で直接的な聞き方です。？
What are the company growth trends?

```
<a id="cli-output"></a>

## 🖥️ CLI Output

## System Initialization

![Initialization](https://github.com/user-attachments/assets/7d62ce1a-cf81-42d8-b7c5-b2ab009a1187)


## Retrieval & Response Generation

![Chatbot Demo](https://github.com/user-attachments/assets/2f4a65fb-5587-427b-9c6a-4bd981f59b53)

## ⚙️ How It Works

1. Load multilingual financial documents
2. Split into chunks
3. Generate embeddings
4. Store in FAISS
5. Retrieve relevant chunks
6. Generate grounded response using TinyLlama

## 🛠️ Tech Stack

- Python
- PyMuPDF
- BAAI-bge-m3
- TinyLlama
- FAISS
- langdetect
- dotenv

<a id="technical-design-decisions"></a>
## Technical Design Decisions
<details>
<summary><strong>Why TinyLlama?</strong></summary>

- 🌍 Open-source and community-driven
- ⚡ Inference speed ↑
- 🧠 Memory consumption ↓
- 💻 Hardware requirements ↓
- 🔄 Development iteration ↑


</details>

<details>
<summary><strong>Why BAAI-BGE-M3?</strong></summary>

BAAI-BGE-M3 was chosen for its strong multilingual semantic retrieval
performance across English and Japanese documents.

Compared to many general embedding models, it provides better
cross-lingual understanding, retrieval accuracy, and efficient
integration with FAISS for RAG-based search.

</details>

<details>
<summary><strong>Why FAISS?</strong></summary>

FAISS was selected for its fast and memory-efficient vector similarity
search capabilities.

Compared to heavier  vector databases, FAISS provides
efficient local semantic retrieval, making it well-suited for scalable
RAG experimentation and multilingual document search.

</details>
<a id="features"></a>

## ✨ Features

- 🌐 Multilingual EN / JP interaction
- 🔍 Semantic retrieval with FAISS
- 🧠 BGE-M3 embedding pipeline
- 🤖 TinyLlama-powered responses
- ✂️ Intelligent document chunking
- 📊 Retrieval transparency & scoring
- 💬 Conversational chatbot memory
- 🏷️ Metadata-aware search
- ⚡ Fast local vector retrieval
- 📁 Cached document preprocessing
- 🔐 `.env`-based configuration
- 🧩 Modular RAG workflow

<a id="pipeline"></a>

## ⚙️ End-to-End Processing Pipeline

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
                            │                                   │
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

## 🚀 Installation & Setup 

### 📥 1. Clone the Repository
```bash
git clone https://github.com/Deepti-vaja/Bilingual-Investor-Relations-Assistant.git
cd Bilingual-Investor-Relations-Assistant
```
### 🐍 2. Create a Virtual Environment
```bash
python -m venv venv
```
### ⚙️ 3. Activate the Virtual Environment
```bash
venv\Scripts\activate
```
### 📦 4. Install Dependencies
```bash
pip install -r requirements.txt
```
### 🔐 5. Environment Variables Setup 
```bash
copy .env.example.env
```
### ▶️ 6. Run the Application
```bash
python main.py
```

## ⚙️ Setup Flow

**Clone → Create venv → Activate venv → Install dependencies → Setup .env → Run project**

<a id="author"></a>
## 👩‍💻 Author

### Deepti Vaja

**AI Developer | RAG Systems | NLP | Python**  

📌 Passionate about building AI intelligence systems.  

🚀 Exploring AI, Machine Learning, GenAI, LLMs for business insights.

- GitHub: [@Deepti-vaja](https://github.com/Deepti-vaja)
- LinkedIn: [@Deepti-vaja linkedin](https://www.linkedin.com/in/deepti-nitesh-vaja-3485402a7/)


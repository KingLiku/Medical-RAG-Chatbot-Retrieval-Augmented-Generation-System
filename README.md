# 🏥 Medical RAG Chatbot: Retrieval-Augmented Generation System

[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-red.svg?style=for-the-badge)](https://www.langchain.com/)
[![Groq API](https://img.shields.io/badge/Groq-Llama_3.3-orange.svg?style=for-the-badge)](https://console.groq.com/)
[![Vector Store](https://img.shields.io/badge/FAISS-CPU-lightgrey.svg?style=for-the-badge)](https://github.com/facebookresearch/faiss)

An advanced, production-grade **Retrieval-Augmented Generation (RAG) chatbot** designed to ingest complex medical reference documents and deliver highly accurate, context-aware answers.

This application uses a local **FAISS** index with **HuggingFace text embeddings** to retrieve relevant clinical text blocks and constructs custom prompts executed on the cloud-hosted **Llama-3.3-70b-versatile** model via **Groq** for rapid, precise inference.

---

## 📐 System Architecture

The workflow below illustrates how documents are loaded, vectorized, indexed, and retrieved to answer user queries:

```mermaid
graph TD
    %% Styling
    classDef storage fill:#2b2b2b,stroke:#ffa500,stroke-width:2px,color:#fff;
    classDef process fill:#1f3c4d,stroke:#00ffcc,stroke-width:1.5px,color:#fff;
    classDef external fill:#4a154b,stroke:#e01e5a,stroke-width:1.5px,color:#fff;

    %% Ingestion Flow
    subgraph Ingestion_Pipeline ["Ingestion Pipeline (Offline)"]
        A["Medical PDFs (data/)"] -->|PyPDF DirectoryLoader| B("Text Ingestion & Parsing")
        B -->|RecursiveCharacterTextSplitter| C("Text Chunking (size: 500, overlap: 50)")
        C -->|sentence-transformers/all-MiniLM-L6-v2| D("Generate Semantic Embeddings")
        D -->|Save Locally| E[("FAISS Vector Index (vectorstore/)")]:::storage
    end

    %% Query / Generation Flow
    subgraph Query_Runtime ["Query Runtime (Online)"]
        F["User Prompt (Flask UI)"] -->|Form Submission| G("Retrieval-QA Chain")
        E -.->|Similarity Search (k=1)| H("Context Retrieval")
        G -->|Fetch Local Context| H
        H -->|Context + Question| I("Custom Prompt Construction")
        I -->|Inference Payload| J("ChatGroq (Llama-3.3-70b)"):::external
        J -->|JSON Response| K("Response Formatting (Flask UI)")
    end

    class B,C,D,G,H,I,K process;
```

---

## 🛠️ Tech Stack & Engineering Specs

- **Backend Framework:** Flask (Python) with Flask-session caching for conversational persistence.
- **RAG Orchestrator:** LangChain (`RetrievalQA` pipeline & `PromptTemplate`).
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2` via HuggingFace (converts chunks to 384-dimensional dense vectors).
- **Vector Database:** Facebook AI Similarity Search (FAISS) local CPU index.
- **Inference LLM:** Groq Chat SDK (`llama-3.3-70b-versatile`) for sub-second, context-based response generation.
- **Robust Exception Handling:** Standardized error wrapping via `CustomException` that intercepts stack traces and exposes file names/line numbers for debugging.
- **Logging Infrastructure:** Daily rotating logs written under `logs/` directory using Python's standard `logging`.

---

## 📁 Project Directory Structure

```text
Medical Project/
│
├── app/
│   ├── common/                  # Shared utilities
│   │   ├── custom_exception.py  # Structured trace logging
│   │   └── logger.py            # Daily-rotating logs configuration
│   │
│   ├── components/              # Modular component layers
│   │   ├── data_loader.py       # Initiates vector DB build
│   │   ├── embedding.py         # Loads HuggingFace model
│   │   ├── llm.py               # Configures Groq Chat SDK
│   │   ├── load_pdf.py          # Handles parsing & text-splitting
│   │   ├── retriever.py         # Configures PromptTemplate & RetrievalQA
│   │   └── vector_store.py      # Handles FAISS save/load
│   │
│   ├── config/                  # Configuration & Environment bindings
│   │   └── config.py
│   │
│   ├── templates/               # Flask UI
│   │   └── index.html           # Dynamic chat UI
│   │
│   └── application.py           # Application entry-point (Flask server)
│
├── data/                        # Raw Medical PDFs (Git-Ignored)
├── logs/                        # System Logs (Git-Ignored)
├── vectorstore/                 # Compiled FAISS Databases (Git-Ignored)
│
├── .env.example                 # Credentials template
├── .gitignore                   # Standard repo file-exclusions
├── req.txt                      # Dependencies specification
├── setup.py                     # Setup wrapper script
└── README.md                    # This document
```

---

## 🚀 Installation & Local Setup

To set up and run this application locally, follow these steps:

### 1. Clone & Set Up the Repository
```bash
git clone https://github.com/your-username/medical-rag-chatbot.git
cd medical-rag-chatbot
```

### 2. Configure Virtual Environment
Create and activate a virtual environment to manage dependencies securely:
```bash
# Create environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate
```

### 3. Install Required Packages
```bash
pip install -r req.txt
```
*(Optional: Install the package in editable mode to bind the root directory)*
```bash
pip install -e .
```

### 4. Setup Secrets Configuration
1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
2. Open the newly created `.env` file and input your Groq API Key:
   ```env
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
   *(Get your free API Key from the [Groq Console](https://console.groq.com/))*

### 5. Index the Source Knowledge (First Time Only)
1. Create a `data/` folder in the root directory.
2. Put any reference PDFs inside the `data/` directory (e.g., medical books, journal articles, or clinical guidelines).
3. Execute the processing pipeline to parse, chunk, and index the text:
   ```bash
   python app/components/data_loader.py
   ```
   This will construct a local FAISS index inside the `vectorstore/` folder.

### 6. Run the Chatbot
Start the Flask development server:
```bash
python app/application.py
```
Open your web browser and go to: **`http://localhost:5000`**

---

## 💡 Engineering Highlights for Recruiters

* **Decoupled Architecture:** Follows a strict separations-of-concern pattern. The data loaders, embeddings, vector indexing, inference LLM, and presentation layer (Flask UI) are independent python modules.
* **Safe Credential Handling:** API keys are never hardcoded and are loaded strictly from system environment/dotenv files.
* **Smart Text Chunking:** Employs a recursive character text splitter with chunk size of 500 characters and an overlap of 50 characters, ensuring semantic consistency across chunks.
* **Robust Error Interceptor:** Uses a custom exception handling pattern (`CustomException`) that identifies the exact filename and line number where an exception occurred, logged directly into daily rotating logs under `logs/`.
* **Resource Optimization:** Utilizes `FAISS.load_local` with `allow_dangerous_deserialization=True` to retrieve context vectors quickly in-memory without incurring expensive API fees or slow DB calls.

## 📱 User Interface Preview
![Chatbot UI Demo](medical\ui-demo.png)

# 🤖 LangOllama — Your Personal AI Assistant

LangOllama is a **local AI assistant** powered by **LangChain + Ollama**, built to answer user queries conversationally using open-source LLMs — all **without any external API calls**.

> 🧩 This is **v1.0 (Basic Chat Assistant)** — a lightweight foundation for the upcoming **LangOllama Pro**, which will include PDF/Text summarization and advanced RAG workflows.

---

## 🚀 Features
- ⚡ **Local LLM Integration** — uses Ollama to run models like Llama3 locally.
- 🧠 **LangChain Framework** — handles prompt management and response parsing.
- 💬 **Chat-based Interaction** — simple, conversational command-line interface.
- 🔒 **Completely Offline** — no API keys or cloud calls required.

---

## 🏗️ Tech Stack
| Layer | Tool / Framework |
|-------|------------------|
| Backend LLM | [Ollama](https://ollama.ai/) |
| Framework | [LangChain](https://www.langchain.com/) |
| Language | Python |
| Environment | Localhost (127.0.0.1:11434) |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/aarthireddyyy/LangOllama.git
cd LangOllama
```
### 2️⃣ Create Virtual Environment
```bash
Copy code
python -m venv lc-env
lc-env\Scripts\activate  # on Windows
```
### 3️⃣ Install Dependencies
```bash
Copy code
pip install -r requirements.txt
```
### 4️⃣ Run Ollama
Make sure Ollama is installed and running:

```bash
Copy code
ollama serve
```
🧠 Ollama runs locally at http://localhost:11434

### 5️⃣ Launch LangOllama
```bash
Copy code
python main.py
Ask any question in the terminal and get an AI-generated response 💬
```
### 🖼️ Demo Screenshots

# Ollama Server	

<img width="954" height="231" alt="Screenshot 2025-10-08 094007" src="https://github.com/user-attachments/assets/200cc055-0058-402e-ba65-bb9d0f12f96d" />

----------------------------

# Chat Interaction
<img width="1847" height="546" alt="Screenshot 2025-10-08 001429" src="https://github.com/user-attachments/assets/100323a2-3954-4793-b796-2484e6e463c1" />

import os

# Centralized configuration for Project ZIN
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT, "data", "assistant_data.db")
NOTES_PATH = os.path.join(ROOT, "data", "notes.txt")
OLLAMA_MODEL = "mistral"   # default local LLM
DEFAULT_TONE = "formal"
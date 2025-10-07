 
#!/usr/bin/env python3
import argparse
import sqlite3
import json
import os
from assistant.config import DB_PATH, NOTES_PATH, OLLAMA_MODEL, DEFAULT_TONE
from assistant.utils import log
from pypdf import PdfReader

# -----------------------
# Persistence helpers
# -----------------------
def save_history(query: str, response: str):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (query, response) VALUES (?, ?)", (query, response))
    conn.commit()
    conn.close()

def fetch_history(limit=10):
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, query, response, timestamp FROM history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# -----------------------
# LLM / model interface
# -----------------------
# Replace old Ollama import
from langchain_ollama.llms import OllamaLLM

# Initialize the model
llm = OllamaLLM(model="mistral")

def generate_response(prompt: str) -> str:
    """Use Ollama via LangChain for real AI responses."""
    try:
        return llm(prompt)
    except Exception as e:
        log(f"❌ Error generating AI response: {e}", "error")
        return "[ERROR] Could not generate response."
# -----------------------
# Command handlers
# -----------------------
def cmd_ask(args):
    prompt = args.query
    log(f"Sending prompt: {prompt[:100]}...", "info")
    response = generate_response(prompt)
    print("\n" + response + "\n")
    save_history(prompt, response)
    log("Saved to history.", "success")

def cmd_summarize_txt(args):
    path = args.path
    if not os.path.exists(path):
        log(f"File not found: {path}", "error")
        return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    prompt = f"Summarize this text in 5 bullet points:\n\n{text}"
    out = generate_response(prompt)
    out_path = os.path.join("data", f"summary_{os.path.basename(path)}.txt")
    with open(out_path, "w", encoding="utf-8") as fo:
        fo.write(out)
    print(out)
    log(f"Summary saved to {out_path}", "success")
    save_history(f"summarize_txt:{path}", out)

def cmd_summarize_pdf(args):
    path = args.path
    if not os.path.exists(path):
        log(f"PDF not found: {path}", "error")
        return
    reader = PdfReader(path)
    text = "\n".join([p.extract_text() or "" for p in reader.pages])
    prompt = f"Summarize this PDF in 8 bullet points:\n\n{text}"
    out = generate_response(prompt)
    out_path = os.path.join("data", f"summary_{os.path.basename(path)}.txt")
    with open(out_path, "w", encoding="utf-8") as fo:
        fo.write(out)
    print(out)
    log(f"PDF summary saved to {out_path}", "success")
    save_history(f"summarize_pdf:{path}", out)

def cmd_email(args):
    to = args.to
    subject = args.subject
    tone = args.tone or DEFAULT_TONE
    context = args.context or ""
    prompt = f"Write a {tone} email to {to} about {subject}. Context: {context}"
    out = generate_response(prompt)
    out_path = os.path.join("data", f"email_{to.replace(' ', '_')}.txt")
    with open(out_path, "w", encoding="utf-8") as fo:
        fo.write(out)
    print(out)
    log(f"Email draft saved to {out_path}", "success")
    save_history(f"email:{to}:{subject}", out)

def cmd_history(args):
    rows = fetch_history(limit=args.limit)
    if not rows:
        log("No history found.", "warning")
        return
    for r in rows:
        print(f"#{r[0]} | {r[3]}\nQ: {r[1]}\nA: {r[2][:400]}...\n{'-'*40}")

def cmd_export_json(args):
    rows = fetch_history(limit=1000000)
    data = [{"id": r[0], "query": r[1], "response": r[2], "timestamp": r[3]} for r in rows]
    out_path = args.path
    with open(out_path, "w", encoding="utf-8") as fo:
        json.dump(data, fo, indent=2)
    log(f"Exported {len(data)} records to {out_path}", "success")

# -----------------------
# CLI wiring
# -----------------------
def build_parser():
    p = argparse.ArgumentParser(prog="assistant/core.py", description="Project ZIN CLI Assistant")
    sp = p.add_subparsers(dest="cmd")

    a = sp.add_parser("ask"); a.add_argument("query", type=str); a.set_defaults(func=cmd_ask)
    b = sp.add_parser("summarize_txt"); b.add_argument("path", type=str); b.set_defaults(func=cmd_summarize_txt)
    c = sp.add_parser("summarize_pdf"); c.add_argument("path", type=str); c.set_defaults(func=cmd_summarize_pdf)
    d = sp.add_parser("email")
    d.add_argument("--to", required=True)
    d.add_argument("--subject", required=True)
    d.add_argument("--tone", required=False)
    d.add_argument("--context", required=False)
    d.set_defaults(func=cmd_email)
    e = sp.add_parser("history"); e.add_argument("--limit", type=int, default=10); e.set_defaults(func=cmd_history)
    f = sp.add_parser("export_json"); f.add_argument("path", type=str); f.set_defaults(func=cmd_export_json)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()

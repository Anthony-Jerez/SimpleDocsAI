import os
import json
import uuid
from typing import List
from .config import DOCS_DIR, SUMMARIES_DIR, ANSWERS_DIR

def new_doc_id() -> str:
    return uuid.uuid4().hex[:12]

def docs_json_path(doc_id: str) -> str:
    return os.path.join(DOCS_DIR, f"{doc_id}.json")

def summaries_json_path(doc_id: str) -> str:
    return os.path.join(SUMMARIES_DIR, f"{doc_id}.json")

def answers_json_path(doc_id: str) -> str:
    return os.path.join(ANSWERS_DIR, f"{doc_id}.json")

def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_to_docs(pages: List[str]):
    """Utility view for human checks."""
    return [{"page": i+1, "text": t[:200]} for i, t in enumerate(pages)]

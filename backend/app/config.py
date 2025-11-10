import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", "./data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
DOCS_DIR = os.path.join(DATA_DIR, "docs")
SUMMARIES_DIR = os.path.join(DATA_DIR, "summaries")
ANSWERS_DIR = os.path.join(DATA_DIR, "answers")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", "gpt-4o-mini")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "Rachel")

# Ensure dirs exist
for d in [DATA_DIR, UPLOAD_DIR, DOCS_DIR, SUMMARIES_DIR, ANSWERS_DIR, CHROMA_PERSIST_DIR]:
    os.makedirs(d, exist_ok=True)

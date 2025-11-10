import os
import fitz
import chromadb
from typing import List
from llama_index.core import Document, VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from .config import (UPLOAD_DIR, CHROMA_PERSIST_DIR, OPENAI_EMBED_MODEL,
                     OPENAI_LLM_MODEL)
from .utils import save_json, docs_json_path

# Configure LlamaIndex globals once
Settings.embed_model = OpenAIEmbedding(model=OPENAI_EMBED_MODEL)
Settings.llm = OpenAI(model=OPENAI_LLM_MODEL, temperature=0.2)

def extract_pages(pdf_path: str) -> List[str]:
    """Extract text (no OCR). If a page is image-only, you'll see little text."""
    pages = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            pages.append(page.get_text("text").strip())
    return pages

def chroma_client():
    # Single persistent client across docs
    return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

def collection_name(doc_id: str) -> str:
    return f"doc_{doc_id}"

def get_collection(doc_id: str):
    return chroma_client().get_or_create_collection(collection_name(doc_id), metadata={"hnsw:space": "cosine"})

def build_index_for_doc(doc_id: str, pages: List[str]) -> int:
    """Create a fresh VectorStoreIndex for this doc_id."""
    # 1) Save raw pages for later (summary verification, display, etc)
    save_json(docs_json_path(doc_id), {"doc_id": doc_id, "pages": pages})

    # 2) Build LlamaIndex documents with metadata (page numbers)
    docs = []
    for i, text in enumerate(pages):
        if not text:
            continue
        docs.append(Document(text=text, metadata={"doc_id": doc_id, "page": i+1}))

    # 3) Connect Chroma as vector store (per-doc collection keeps things simple)
    vs = ChromaVectorStore(chroma_collection=get_collection(doc_id))
    sc = StorageContext.from_defaults(vector_store=vs)

    # 4) Index (this will chunk + embed automatically using Settings.embed_model)
    VectorStoreIndex.from_documents(docs, storage_context=sc)
    return len(docs)

def save_upload(file, doc_id: str) -> str:
    dest = os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")
    with open(dest, "wb") as out:
        out.write(file)
    return dest

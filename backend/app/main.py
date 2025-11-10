from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io

from .utils import new_doc_id, load_json, summaries_json_path, answers_json_path, save_json
from .ingestion import save_upload, extract_pages, build_index_for_doc
from .summarize import summarize_spanish
from .ask import answer_spanish

app = FastAPI(title="Doc Summarizer Backend (EN→ES)")

# CORS (open for local testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

# ingest
class IngestResponse(BaseModel):
    doc_id: str
    pages: int
    chunks_indexed: int

@app.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...), doc_id: str = Form(None)):
    """
    Upload a PDF, extract pages, build a per-doc Chroma collection, and index with OpenAI embeddings.
    """
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Please upload a PDF.")
    doc_id = doc_id or new_doc_id()

    # Save upload
    raw = await file.read()
    pdf_path = save_upload(raw, doc_id)

    # Extract
    pages = extract_pages(pdf_path)
    if not any(pages):
        # (optional) here can trigger OCR fallback
        raise HTTPException(status_code=422, detail="No extractable text found. (Try OCR fallback in future.)")

    # Index
    count = build_index_for_doc(doc_id, pages)
    return IngestResponse(doc_id=doc_id, pages=len(pages), chunks_indexed=count)

# summarize
class SummarizeBody(BaseModel):
    doc_id: str

@app.post("/summarize")
def summarize(body: SummarizeBody):
    out = summarize_spanish(body.doc_id)
    return out

# /ask
class AskBody(BaseModel):
    doc_id: str
    query_es: str
    top_k: int = 6

@app.post("/ask")
def ask(body: AskBody):
    ans = answer_spanish(body.doc_id, body.query_es, body.top_k)
    # Save a trace for debugging
    save_json(answers_json_path(body.doc_id), ans)
    return ans

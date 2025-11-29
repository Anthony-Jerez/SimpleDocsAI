from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .utils import new_doc_id, load_json, summaries_json_path, answers_json_path, save_json
from .ingestion import save_upload, extract_pages, build_index_for_doc
from .summarize import summarize_spanish
from .ask import answer_spanish
from fastapi.staticfiles import StaticFiles
from .config import AUDIO_DIR
from pydantic import BaseModel, Field
from typing import Optional
from .config import LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET
from .tokens import mint_join_token
from .summarize_text import summarize_text_to_spanish

app = FastAPI(title="Doc Summarizer Backend (EN->ES)")
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

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


class TokenRequest(BaseModel):
    room: str = Field(..., description="Room name to join (will be auto-created on first join)")
    identity: Optional[str] = Field(None, description="Participant identity (optional, server will generate if empty)")
    name: Optional[str] = Field(None, description="Display name (optional)")
    can_publish: bool = True
    can_subscribe: bool = True

class TokenResponse(BaseModel):
    token: str
    url: str
    room: str
    identity: str

@app.get("/livekit/health")
def livekit_health():
    ok = bool(LIVEKIT_URL and LIVEKIT_API_KEY and LIVEKIT_API_SECRET)
    return {
        "livekit_configured": ok,
        "url_present": bool(LIVEKIT_URL),
        "api_key_present": bool(LIVEKIT_API_KEY),
        "api_secret_present": bool(LIVEKIT_API_SECRET),
    }

@app.post("/livekit/token", response_model=TokenResponse)
def livekit_token(req: TokenRequest):
    if not LIVEKIT_URL or not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
        raise HTTPException(status_code=500, detail="LiveKit env vars missing")

    token, identity = mint_join_token(
        room=req.room,
        identity=req.identity,
        name=req.name,
        can_publish=req.can_publish,
        can_subscribe=req.can_subscribe,
    )
    return TokenResponse(token=token, url=LIVEKIT_URL, room=req.room, identity=identity)

class SummarizeTextBody(BaseModel):
    text: str
    # Future-proof: you can widen later; for now we only support Spanish output.
    target_lang: str = "es"

class SummarizeTextResp(BaseModel):
    doc_id: str
    summary_es: str
    audio_url: Optional[str] = None

@app.post("/summarize_text", response_model=SummarizeTextResp)
def summarize_text_api(body: SummarizeTextBody):
    """
    Direct LLM summary for pasted text (EN -> ES). No RAG.
    Returns same shape as /summarize so the frontend can render identically.
    """
    if body.target_lang != "es":
        # MVP: we only support Spanish; later you can branch prompts by lang code.
        raise HTTPException(status_code=400, detail="Only 'es' is supported for now.")

    out = summarize_text_to_spanish(body.text)
    # Use a synthetic doc_id to satisfy the same shape as PDF summarize.
    return {"doc_id": "text_snippet", **out}

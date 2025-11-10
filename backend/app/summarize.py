from typing import Dict, List
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from .ingestion import get_collection
from .utils import load_json, summaries_json_path, save_json, docs_json_path

llm = OpenAI(temperature=0.2)  # uses OPENAI_LLM_MODEL from Settings

MAP_PROMPT_ES = """Eres un asistente claro y paciente. Resume en ESPAÑOL este fragmento para padres, a nivel de 6.º grado.
Incluye: (1) puntos clave, (2) qué significa para mí, (3) fechas y montos, (4) próximos pasos, (5) definiciones de jerga.
Usa un estilo breve y natural. No inventes nada. Cita la página como [p:{page}].
TEXTO (inglés, página {page}):
---
{chunk}
---
Salida (breve, con viñetas y [p:{page}]):"""

REDUCE_PROMPT_ES = """Combina y deduplica los mini-resúmenes en un resumen único en ESPAÑOL (nivel 6.º grado).
Estructura la salida como:

## TL;DR (3-5 viñetas)
- ...
## Qué significa para mí
- ...
## Fechas y montos
- ...
## Próximos pasos
1) ...
## Definiciones
- Término: explicación breve

Conserva las citas de página tal como [p:X] al final de cada viñeta.
No agregues información no respaldada por los mini-resúmenes.
Mini-resúmenes:
---
{mini_summaries}
---
Resumen final (ES):"""

def get_index(doc_id: str) -> VectorStoreIndex:
    vs = ChromaVectorStore(chroma_collection=get_collection(doc_id))
    return VectorStoreIndex.from_vector_store(vs)

def _select_cover_nodes(index: VectorStoreIndex, k: int = 20) -> List[str]:
    """Retrieve a coverage set by issuing a few broad Spanish queries."""
    retriever = index.as_retriever(similarity_top_k=k)
    seeds = [
        "Resumen de los puntos principales",
        "Fechas límites y cantidades importantes",
        "Pasos necesarios o acciones requeridas",
        "Definiciones y términos clave",
    ]
    texts = []
    seen = set()
    for q in seeds:
        for n in retriever.retrieve(q):
            t = n.node.get_content().strip()
            if t and t not in seen:
                texts.append((n.node.metadata.get("page", 0), t))
                seen.add(t)
    # sort by page to keep narrative roughly aligned
    texts.sort(key=lambda x: x[0])
    return [f"[p:{p}] {t}" for p, t in texts]

def summarize_spanish(doc_id: str) -> Dict:
    """Map→Reduce Spanish summary grounded on the English text."""
    # Load raw pages to assist with per-page map step
    raw = load_json(docs_json_path(doc_id))
    pages = raw.get("pages", [])

    # Build index wrapper (for later verification/expansion if needed)
    index = get_index(doc_id)

    # MAP: summarize each page's most relevant spans (use a coverage set instead of all pages)
    cover_nodes = _select_cover_nodes(index, k=24)
    mini_summaries = []
    for item in cover_nodes:
        # item looks like "[p:X] text..."
        # extract page
        try:
            prefix, chunk = item.split("] ", 1)
            page = int(prefix.replace("[p:", ""))
        except Exception:
            page, chunk = 0, item

        msg = MAP_PROMPT_ES.format(page=page or "?", chunk=chunk[:4000])
        mini_summaries.append(llm.complete(msg).text.strip())

    # REDUCE: combine all mini summaries into a single parent-friendly summary
    reduce_in = "\n\n".join(mini_summaries)
    final_summary = llm.complete(REDUCE_PROMPT_ES.format(mini_summaries=reduce_in)).text.strip()

    # Save & return
    out = {"doc_id": doc_id, "summary_es": final_summary, "mini": mini_summaries}
    save_json(summaries_json_path(doc_id), out)
    return out

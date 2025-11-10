from typing import Dict, List, Any
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
from .ingestion import get_collection

# For more ore deterministic outputs
llm = OpenAI(temperature=0.1)

ANSWER_PROMPT_ES = """Eres un asistente claro y preciso. Responde en ESPAÑOL (nivel 6.º grado).
Usa SOLO la información del CONTEXTO. Si no está en el contexto, di que no aparece.
Incluye citas de página como [p:X] al final de las oraciones relevantes. Sé breve (3-6 oraciones).
Si el CONTEXTO nombra a la persona o rol responsable o describe criterios/condiciones, menciónalos tal cual.
Incluye 1-2 citas textuales cortas (entre comillas) para soportar afirmaciones clave.

PREGUNTA (ES): {question}

CONTEXTO (inglés con metadatos de página):
---
{context}
---
RESPUESTA (ES):"""

def get_index(doc_id: str) -> VectorStoreIndex:
    vs = ChromaVectorStore(chroma_collection=get_collection(doc_id))
    return VectorStoreIndex.from_vector_store(vs)

def answer_spanish(doc_id: str, query_es: str, top_k: int = 6) -> Dict[str, Any]:
    index = get_index(doc_id)
    retriever = index.as_retriever(similarity_top_k=top_k)

    # Multilingual embeddings
    nodes = retriever.retrieve(query_es)

    if not nodes:
        return {
            "doc_id": doc_id,
            "question_es": query_es,
            "answer_es": "No encontré información relevante en el documento.",
            "citations": [],
            "retrieved": [],
            "context": ""
        }

    # Build both: (a) context string used for prompting and (b) a structured list to inspect
    retrieved: List[Dict[str, Any]] = []
    ctx_lines: List[str] = []

    for rank, n in enumerate(nodes[:top_k], start=1):
        page = n.node.metadata.get("page", "?")
        raw = n.node.get_content() or ""
        text = " ".join(raw.split())  # normalize whitespace
        score = getattr(n, "score", None)
        node_id = getattr(n.node, "node_id", None)

        retrieved.append({
            "rank": rank,
            "page": page,
            "score": score,
            "node_id": node_id,
            "text": text[:1200]
        })
        ctx_lines.append(f"[p:{page}] {text}")

    context = "\n".join(ctx_lines)
    answer = llm.complete(
        ANSWER_PROMPT_ES.format(question=query_es, context=context)
    ).text.strip()

    return {
        "doc_id": doc_id,
        "question_es": query_es,
        "answer_es": answer,
        "citations": [n.node.metadata.get("page", None) for n in nodes[:top_k]],
        "retrieved": retrieved, # structured English snippets (rank/page/score/text)
        "context": context # exact block passed to the LLM
    }

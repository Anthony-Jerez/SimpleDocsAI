from typing import Dict, Optional
from llama_index.llms.openai import OpenAI
from .tts import synthesize_and_cache  # returns (abs_path, /audio/<file>.mp3) or (None, None)

# Configure to use global OPENAI_LLM_MODEL via LlamaIndex Settings (already configured elsewhere)
llm = OpenAI(temperature=0.2)

PROMPT_SUMMARY_ES = """Eres un asistente claro y paciente.
Lee el TEXTO (en inglés) y devuelve un resumen en ESPAÑOL (nivel 6.º grado).

Estructura:
## TL;DR (3-5 viñetas)
- ...
## Qué significa para mí
- ...
## Próximos pasos
1) ...
## Definiciones
- Término: explicación breve

No inventes datos. Responde solo con el resumen.

TEXTO:
---
{snippet}
---
"""

def summarize_text_to_spanish(text: str) -> Dict[str, Optional[str]]:
    """
    Direct LLM path for small pasted text (no RAG).
    Returns {"summary_es": ..., "audio_url": ...}
    """
    snippet = (text or "").strip()
    if not snippet:
        return {"summary_es": "", "audio_url": None}

    # keep prompt size reasonable (characters; safe for typical inputs)
    snippet = snippet[:8000]

    summary = llm.complete(PROMPT_SUMMARY_ES.format(snippet=snippet)).text.strip()

    # Optional: TTS (cached). Will be None if ELEVENLABS_* not set.
    _, rel_url = synthesize_and_cache(summary)

    return {"summary_es": summary, "audio_url": rel_url}

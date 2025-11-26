import os
import hashlib
import requests
from typing import Optional, Tuple
from .config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, AUDIO_DIR

ELEVEN_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

MODEL_ID = "eleven_multilingual_v2"  # Good default for ES and other languages

def _hash_key(text: str, voice_id: str, model_id: str = MODEL_ID) -> str:
    norm = " ".join((text or "").split()).strip()
    h = hashlib.sha256(f"{voice_id}|{model_id}|{norm}".encode("utf-8")).hexdigest()
    return h

def synthesize_and_cache(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Returns (abs_path, rel_url). If TTS disabled/missing config, returns (None, None).
    """
    if not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
        return None, None

    key = _hash_key(text, ELEVENLABS_VOICE_ID, MODEL_ID)
    filename = f"{key}.mp3"
    abs_path = os.path.join(AUDIO_DIR, filename)
    rel_url = f"/audio/{filename}"

    if os.path.exists(abs_path) and os.path.getsize(abs_path) > 0:
        return abs_path, rel_url

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "accept": "audio/mpeg",
        "content-type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }
    url = ELEVEN_TTS_URL.format(voice_id=ELEVENLABS_VOICE_ID)

    with requests.post(url, headers=headers, json=payload, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(abs_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return abs_path, rel_url

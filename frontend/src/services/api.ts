const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000';

function toAbsolute(url?: string | null) {
  if (!url) return url ?? undefined;
  try { return new URL(url).toString(); }
  catch {
    const needsSlash = url.startsWith('/') ? '' : '/';
    return `${API_BASE}${needsSlash}${url}`;
  }
}

export function newDocId() {
  return `doc_${Math.random().toString(36).slice(2, 10)}`;
}

export type SummarizeResp = { doc_id: string; summary_es: string; audio_url?: string }
export type IngestResp = { doc_id: string; pages: number; chunks_indexed: number }
export type AskResp = { doc_id: string; question_es: string; answer_es: string; citations: number[]; context?: string }

export async function ingestPdf(file: File, docId?: string): Promise<IngestResp> {
  const id = docId || newDocId();
  const fd = new FormData();
  fd.append('file', file);
  fd.append('doc_id', id);
  const res = await fetch(`${API_BASE}/ingest`, { method: 'POST', body: fd });
  if (!res.ok) throw new Error('Ingest failed');
  const data = await res.json();
  return data;
}

export async function summarize(docId: string): Promise<SummarizeResp> {
  const res = await fetch(`${API_BASE}/summarize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ doc_id: docId })
  });
  if (!res.ok) throw new Error('Summarize failed');
  const data = await res.json();
  (data as any).audio_url = toAbsolute(data.audio_url);
  return data;
}

export async function summarizeText(
  text: string,
  targetLang: string = 'es'
): Promise<SummarizeResp> {
  const res = await fetch(`${API_BASE}/summarize_text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, target_lang: targetLang }),
  });
  if (!res.ok) throw new Error('Summarize text failed');
  const data = await res.json();
  (data as any).audio_url = toAbsolute(data.audio_url);
  return data;
}

export async function ask(docId: string, queryEs: string): Promise<AskResp> {
  const res = await fetch(`${API_BASE}/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ doc_id: docId, query_es: queryEs, top_k: 6 })
  });
  if (!res.ok) throw new Error('Ask failed');
  return res.json();
}

export async function mintLivekitToken(room: string, name?: string) {
  const res = await fetch(`${API_BASE}/livekit/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ room, name })
  });
  if (!res.ok) throw new Error('Token mint failed');
  return res.json() as Promise<{ token: string; url: string; room: string; identity: string }>;
}

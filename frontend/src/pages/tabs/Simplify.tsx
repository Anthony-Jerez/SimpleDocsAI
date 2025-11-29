import { useRef, useState } from 'react'
import LanguageSelect from '../../components/LanguageSelect'
import { ingestPdf, summarize, summarizeText } from '../../services/api'

function PaperclipIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M21.44 11.05 12 20.5a6 6 0 1 1-8.49-8.49l10-10a4 4 0 1 1 5.66 5.66L8.5 18.34a2 2 0 1 1-2.83-2.83l9.2-9.2"/>
    </svg>
  )
}

export default function Simplify({
  onSummary,
}: {
  onSummary?: (summary: string, audio?: string) => void
}) {
  const [lang, setLang] = useState('es')
  const [text, setText] = useState('')
  const [busy, setBusy] = useState(false)
  const [status, setStatus] = useState('')
  const fileRef = useRef<HTMLInputElement | null>(null)

  async function handleFile(file: File) {
    try {
      setBusy(true)
      setStatus('Uploading & indexing…')
      // we use a fixed doc_id for now (backend already working)
      await ingestPdf(file, 'mydoc1')
      setStatus('Summarizing…')
      const res = await summarize('mydoc1')
      onSummary?.(res.summary_es, res.audio_url)
      setStatus('Done!')
    } catch (e: any) {
      setStatus(e.message || 'Failed')
    } finally {
      setBusy(false)
    }
  }

  function onPick() {
    fileRef.current?.click()
  }

  async function onSubmitText() {
    if (!text.trim()) return
    try {
      setBusy(true);
      setStatus('Summarizing text…');
      const res = await summarizeText(text, lang); // backend currently supports 'es' only
      onSummary?.(res.summary_es, res.audio_url);
      setStatus('Done!');
    } catch (e: any) {
      setStatus(e.message || 'Failed');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm text-sub mb-1">Translate response to</label>
        <LanguageSelect value={lang} onChange={setLang} />
      </div>

      <div>
        <label className="block text-sm text-sub mb-1">Ask a question or paste text to simplify…</label>
        <div className="relative">
          <textarea
            className="textarea pr-40"
            placeholder="Paste text here… (or use the paperclip to upload a PDF)"
            rows={6}
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <div className="absolute right-2 bottom-2 flex items-center gap-2">
            {/* PAPERCLIP ONLY on Simplify */}
            <button
              type="button"
              className="icon-btn icon-btn--ghost"
              aria-label="Upload PDF"
              onClick={onPick}
            >
              <PaperclipIcon />
            </button>
            <input
              ref={fileRef}
              type="file"
              accept="application/pdf"
              className="hidden"
              onChange={(e) => {
                const f = e.target.files?.[0]
                if (f) handleFile(f)
              }}
            />
            <button
              className="btn btn-primary"
              disabled={busy || !text.trim()}
              onClick={onSubmitText}
            >
              {busy ? 'Working…' : 'Summarize'}
            </button>
          </div>
        </div>
      </div>

      <div className="text-xs text-sub">{status}</div>
    </div>
  )
}

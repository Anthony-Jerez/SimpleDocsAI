import { useState } from 'react'
import { ask } from '../../services/api'

function MicIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 14a3 3 0 0 0 3-3V6a3 3 0 1 0-6 0v5a3 3 0 0 0 3 3Z"/>
      <path d="M19 11a7 7 0 0 1-14 0M12 18v3" stroke="currentColor" strokeWidth="2" fill="none" />
    </svg>
  )
}

export default function QATab({
  onAnswer,
}: {
  onAnswer?: (answer: string) => void
}) {
  const [q, setQ] = useState('¿Quién determina si corresponde una sanción disciplinaria además de la académica?')
  const [busy, setBusy] = useState(false)

  async function onAskClick() {
    setBusy(true)
    try {
      const res = await ask('mydoc1', q) // doc selection will be added later
      onAnswer?.(res.answer_es)
    } finally {
      setBusy(false)
    }
  }

  function onMic() {
    // hook up LiveKit later; for now it’s a no-op UI
  }

  return (
    <div className="space-y-3">
      <label className="block text-sm text-sub">Question about the document</label>
      <div className="relative">
        <textarea
          className="textarea pr-40"
          rows={5}
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <div className="absolute right-2 bottom-2 flex items-center gap-2">
          {/* MIC ONLY on Q&A, with brand color */}
          <button
            type="button"
            className="icon-btn icon-btn--mic"
            aria-label="Record"
            onClick={onMic}
            title="Use microphone"
          >
            <MicIcon />
          </button>
          <button
            className="btn btn-primary"
            onClick={onAskClick}
            disabled={busy || !q.trim()}
          >
            {busy ? 'Asking…' : 'Ask'}
          </button>
        </div>
      </div>
    </div>
  )
}

import { useRef } from 'react'


export default function FileUploader({ onFile }: { onFile: (f: File) => void }) {
    const ref = useRef<HTMLInputElement | null>(null)
    return (
        <div className="flex items-center gap-3">
            <input ref={ref} type="file" accept="application/pdf" onChange={e => {
                const f = e.target.files?.[0]
                if (f) onFile(f)
            }} className="hidden" />
            <button className="btn btn-primary" onClick={() => ref.current?.click()}>Choose PDF</button>
        </div>
    )
}
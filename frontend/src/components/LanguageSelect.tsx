const LANGS = [
    { code: 'es', label: 'Español (MVP)' },
    // future: { code: 'fr', label: 'Français' }, { code: 'zh', label: '中文' }, ...
]


export default function LanguageSelect({ value, onChange }: { value: string; onChange: (v: string) => void }) {
    return (
        <select className="select" value={value} onChange={e => onChange(e.target.value)}>
            {LANGS.map(l => <option key={l.code} value={l.code}>{l.label}</option>)}
        </select>
    )
}
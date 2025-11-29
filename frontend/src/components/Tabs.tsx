type Tab = { key: string; label: string }

export default function Tabs({
    tabs,
    active,
    onChange,
}: { tabs: Tab[]; active: string; onChange: (k: string) => void }) {
    return (
        <div className="flex gap-2">
            {tabs.map(t => (
                <button
                    key={t.key}
                    className="tab-btn"
                    data-active={active === t.key}
                    onClick={() => onChange(t.key)}
                >
                    {t.label}
                </button>
            ))}
        </div>
    )
}
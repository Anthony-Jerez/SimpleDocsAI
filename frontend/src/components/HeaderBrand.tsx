export default function HeaderBrand() {
    return (
        <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl2 bg-gradient-to-br from-brand-500 to-brand-700 grid place-items-center shadow-soft">
                <span className="text-white text-xl">🧙‍♂️</span>
            </div>
            <div>
                <div className="text-xl font-semibold">Simple Docs AI</div>
                <div className="text-xs text-sub">Simplify ANY document to ANY language</div>
            </div>
        </div>
    )
}
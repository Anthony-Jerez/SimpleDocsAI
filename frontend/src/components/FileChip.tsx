export default function FileChip({
  name,
  onClear,
}: { name: string; onClear: () => void }) {
  return (
    <div className="inline-flex items-center gap-2 bg-brand-600/20 text-brand-200 px-3 py-1.5 rounded-xl2 border border-brand-500/40">
      <span className="truncate max-w-[220px]">{name}</span>
      <button className="text-brand-200 hover:text-white" onClick={onClear} title="Remove">
        ✕
      </button>
    </div>
  );
}

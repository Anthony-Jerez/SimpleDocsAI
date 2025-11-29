import { useEffect, useRef, useState } from "react";

export default function SplitPane({
  left,
  right,
}: { left: React.ReactNode; right: React.ReactNode }) {
  const [leftPct, setLeftPct] = useState(42); // 25–75%
  const wrapRef = useRef<HTMLDivElement | null>(null);
  const dragging = useRef(false);

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (!dragging.current || !wrapRef.current) return;
      const rect = wrapRef.current.getBoundingClientRect();
      const pct = ((e.clientX - rect.left) / rect.width) * 100;
      setLeftPct(Math.min(75, Math.max(25, pct)));
    };
    const stop = () => (dragging.current = false);

    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", stop);
    window.addEventListener("mouseleave", stop);
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", stop);
      window.removeEventListener("mouseleave", stop);
    };
  }, []);

  return (
    <div ref={wrapRef} className="h-[calc(100vh-64px)]">
      <div className="h-full flex">
        <div style={{ width: `${leftPct}%` }} className="h-full p-4">
          <div className="card h-full p-6">{left}</div>
        </div>

        <div
          className="w-1 bg-white/10 cursor-col-resize hover:bg-white/20"
          onMouseDown={() => (dragging.current = true)}
          title="Drag to resize"
        />

        <div style={{ width: `${100 - leftPct}%` }} className="h-full p-4">
          <div className="card h-full p-6 overflow-auto">{right}</div>
        </div>
      </div>
    </div>
  );
}

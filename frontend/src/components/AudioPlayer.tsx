import { useEffect, useRef, useState } from "react";

/** Simple custom player to match brand colors. */
export default function AudioPlayer({ src }: { src?: string }) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [playing, setPlaying] = useState(false);
  const [t, setT] = useState(0);
  const [dur, setDur] = useState(0);

  useEffect(() => {
    const a = audioRef.current;
    if (!a) return;
    const onTime = () => setT(a.currentTime || 0);
    const onMeta = () => setDur(a.duration || 0);
    const onEnd = () => setPlaying(false);

    a.addEventListener("timeupdate", onTime);
    a.addEventListener("loadedmetadata", onMeta);
    a.addEventListener("ended", onEnd);
    return () => {
      a.removeEventListener("timeupdate", onTime);
      a.removeEventListener("loadedmetadata", onMeta);
      a.removeEventListener("ended", onEnd);
    };
  }, []);

  if (!src) return null;

  const fmt = (s: number) => {
    const m = Math.floor(s / 60);
    const r = Math.floor(s % 60).toString().padStart(2, "0");
    return `${m}:${r}`;
    };

  const toggle = () => {
    const a = audioRef.current;
    if (!a) return;
    if (playing) {
      a.pause();
      setPlaying(false);
    } else {
      a.play().then(() => setPlaying(true));
    }
  };

  const onSeek = (v: number) => {
    const a = audioRef.current;
    if (!a) return;
    a.currentTime = v;
    setT(v);
  };

  return (
    <div className="rounded-xl2 bg-panelElev border border-white/10 p-4">
      <audio ref={audioRef} src={src} preload="metadata" />
      <div className="flex items-center gap-3">
        <button
          className="btn btn-primary h-10 w-10 rounded-full p-0"
          onClick={toggle}
        >
          {playing ? "❚❚" : "►"}
        </button>
        <div className="text-xs tabular-nums text-sub w-12">{fmt(t)}</div>
        <input
          type="range"
          min={0}
          max={dur || 0}
          value={t}
          onChange={(e) => onSeek(Number(e.target.value))}
          className="flex-1 accent-[rgb(168,85,247)]"
        />
        <div className="text-xs tabular-nums text-sub w-12 text-right">
          {fmt(dur || 0)}
        </div>
      </div>
    </div>
  );
}

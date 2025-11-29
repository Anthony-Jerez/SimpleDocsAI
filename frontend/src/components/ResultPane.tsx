import ReactMarkdown from "react-markdown";
import { useAppState } from "../state/AppState";
import AudioPlayer from "./AudioPlayer";

export default function ResultPane() {
  const { summary, audioUrl, qaAnswer } = useAppState();

  const hasAnything = summary || audioUrl || qaAnswer;

  if (!hasAnything) {
    return (
      <div>
        <h2 className="text-xl font-semibold">Welcome to Wizdom</h2>
        <p className="text-sub mt-1">
          Upload a PDF or paste text on the left. Results, translated summaries,
          audio, and Q&amp;A answers will appear here.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {summary && (
        <section>
          <h3 className="text-lg font-semibold mb-2">Translated Summary</h3>
          <div className="prose prose-invert max-w-none">
            <ReactMarkdown>{summary}</ReactMarkdown>
          </div>
        </section>
      )}
      {audioUrl && (
        <section>
          <h3 className="text-lg font-semibold mb-2">Narration</h3>
          <AudioPlayer src={audioUrl} />
        </section>
      )}
      {qaAnswer && (
        <section>
          <h3 className="text-lg font-semibold mb-2">Q&amp;A</h3>
          <div className="leading-relaxed">{qaAnswer}</div>
        </section>
      )}
    </div>
  );
}

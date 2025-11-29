import ReactMarkdown from 'react-markdown'


export default function SummaryView({ summary }: { summary?: string }) {
    if (!summary) return <div className="text-sub">No summary yet.</div>
    return (
        <div className="prose prose-invert max-w-none">
            <ReactMarkdown>{summary}</ReactMarkdown>
        </div>
    )
}
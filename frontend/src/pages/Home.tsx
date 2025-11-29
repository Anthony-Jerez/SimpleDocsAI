import { useState } from 'react'
import Tabs from '../components/Tabs'
import SplitPane from '../components/SplitPane'
import SimplifyTab from './tabs/Simplify'
import QATab from './tabs/QATab'
import SummaryView from '../components/SummaryView'
import AudioPlayer from '../components/AudioPlayer'

export default function Home() {
  const [tab, setTab] = useState<'simplify' | 'qa'>('simplify')
  const [summary, setSummary] = useState<string>()
  const [audio, setAudio] = useState<string>()
  const [answer, setAnswer] = useState<string>()

  return (
    <SplitPane
      left={
        <div className="h-full flex flex-col gap-6">
          <div className="text-3xl font-bold">Simple Docs AI</div>
          <p className="text-sub">Simplify ANY document to ANY language</p>

          <Tabs
            tabs={[
              { key: 'simplify', label: 'Simplify' },
              { key: 'qa', label: 'Ask / Q&A' },
            ]}
            active={tab}
            onChange={(k) => setTab(k as any)}
          />

          <div className="flex-1 overflow-auto">
            {tab === 'simplify' && (
              <SimplifyTab onSummary={(s, a) => { setAnswer(undefined); setSummary(s); setAudio(a) }} />
            )}
            {tab === 'qa' && (
              <QATab onAnswer={(a) => { setSummary(undefined); setAudio(undefined); setAnswer(a) }} />
            )}
          </div>
        </div>
      }
      right={
        <div className="h-full">
          {!summary && !answer ? (
            <>
              <h2 className="text-xl font-semibold">Welcome to Wizdom</h2>
              <p className="text-sub">
                Upload a PDF or paste text on the left. Results, translated summaries, audio, and Q&A answers will appear here.
              </p>
            </>
          ) : (
            <>
              {summary && <SummaryView summary={summary} />}
              {audio && <AudioPlayer src={audio} />}
              {answer && (
                <div className="mt-3 p-4 bg-panelElev rounded-xl2 border border-white/10">
                  <div className="text-sm leading-relaxed whitespace-pre-wrap">{answer}</div>
                </div>
              )}
            </>
          )}
        </div>
      }
    />
  )
}

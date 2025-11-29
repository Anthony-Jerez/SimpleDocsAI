import React, { createContext, useContext, useState } from "react";

type AppStateShape = {
  currentDocId?: string;
  currentDocName?: string;
  summary?: string;
  audioUrl?: string;
  qaAnswer?: string;
  setDoc: (id?: string, name?: string) => void;
  setResult: (summary?: string, audioUrl?: string) => void;
  setQA: (answer?: string) => void;
  clearAll: () => void;
};

const AppState = createContext<AppStateShape | null>(null);

export function AppStateProvider({ children }: { children: React.ReactNode }) {
  const [currentDocId, setDocId] = useState<string | undefined>();
  const [currentDocName, setDocName] = useState<string | undefined>();
  const [summary, setSummary] = useState<string | undefined>();
  const [audioUrl, setAudio] = useState<string | undefined>();
  const [qaAnswer, setQAAnswer] = useState<string | undefined>();

  const setDoc = (id?: string, name?: string) => {
    setDocId(id);
    setDocName(name);
  };

  const setResult = (s?: string, a?: string) => {
    setSummary(s);
    setAudio(a);
  };

  const setQA = (ans?: string) => setQAAnswer(ans);

  const clearAll = () => {
    setSummary(undefined);
    setAudio(undefined);
    setQAAnswer(undefined);
  };

  return (
    <AppState.Provider
      value={{ currentDocId, currentDocName, summary, audioUrl, qaAnswer, setDoc, setResult, setQA, clearAll }}
    >
      {children}
    </AppState.Provider>
  );
}

export function useAppState() {
  const ctx = useContext(AppState);
  if (!ctx) throw new Error("useAppState must be used within AppStateProvider");
  return ctx;
}

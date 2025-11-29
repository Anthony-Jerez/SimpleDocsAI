import { Outlet } from "react-router-dom";
import HeaderBrand from "./components/HeaderBrand";
import { AppStateProvider } from "./state/AppState";

export default function App() {
  return (
    <AppStateProvider>
      <div className="min-h-screen flex flex-col">
        <header className="border-b border-white/5 bg-panel">
          <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
            <HeaderBrand />
            <div className="text-sm text-sub">Dark + High Contrast + v0.1</div>
          </div>
        </header>
        <main className="flex-1">
          <Outlet />
        </main>
      </div>
    </AppStateProvider>
  );
}

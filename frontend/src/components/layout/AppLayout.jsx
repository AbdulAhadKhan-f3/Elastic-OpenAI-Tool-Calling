import { useState } from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import Dashboard from "../../pages/Dashboard";
import ToolsPanel from "../mcp/ToolsPanel";

function AppLayout() {
  const [activeView, setActiveView] = useState("agent");

  return (
    <div className="app-shell">
      <Sidebar activeView={activeView} onViewChange={setActiveView} />

      <div className="main-area">
        <Topbar activeView={activeView} />

        <main className="main-content">
          {activeView === "tools" ? <ToolsPanel /> : <Dashboard />}
        </main>
      </div>
    </div>
  );
}

export default AppLayout;
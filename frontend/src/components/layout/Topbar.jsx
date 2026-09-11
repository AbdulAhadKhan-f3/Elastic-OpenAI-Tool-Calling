import { ChevronDown, CircleHelp, Server } from "lucide-react";

function Topbar({ activeView }) {
  return (
    <header className="topbar">
      <div className="topbar-title">
        <span>{activeView === "tools" ? "MCP Tools" : "Agent Workspace"}</span>
        <ChevronDown size={15} />
      </div>

      <div className="topbar-actions">
        <div className="connection-status">
          <span className="status-dot" />
          <Server size={15} />
          <span>MCP Server</span>
          <strong>Online</strong>
        </div>

        <button className="icon-button" aria-label="Help">
          <CircleHelp size={18} />
        </button>
      </div>
    </header>
  );
}

export default Topbar;
import {
  Bot,
  MessageSquare,
  Plus,
  Settings,
  Wrench,
} from "lucide-react";

function Sidebar({ activeView, onViewChange }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-mark">
          <Bot size={20} strokeWidth={2.2} />
        </div>

        <span>Nexus</span>
      </div>

      <button className="new-chat-button">
        <Plus size={18} />
        <span>New conversation</span>
      </button>

      <div className="sidebar-section">
        <p className="sidebar-label">Workspace</p>

        <nav className="sidebar-nav">
          <button
            className={`sidebar-link ${activeView === "agent" ? "active" : ""}`}
            onClick={() => onViewChange("agent")}
            type="button"
          >
            <MessageSquare size={17} />
            <span>Agent</span>
          </button>

          <button
            className={`sidebar-link ${activeView === "tools" ? "active" : ""}`}
            onClick={() => onViewChange("tools")}
            type="button"
          >
            <Wrench size={17} />
            <span>MCP Tools</span>
          </button>
        </nav>
      </div>


      <div className="sidebar-bottom">
        <a className="sidebar-link" href="#">
          <Settings size={17} />
          <span>Settings</span>
        </a>
      </div>
    </aside>
  );
}

export default Sidebar;
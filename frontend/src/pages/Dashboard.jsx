import {
  Activity,
  Database,
  Search,
  Sparkles,
  Users,
} from "lucide-react";

import ChatWindow from "../components/chat/ChatWindow";
import ChatInput from "../components/chat/ChatInput";
import useChat from "../hooks/useChat";

function Dashboard() {
  const { messages, sendMessage, isLoading } = useChat();

  const hasMessages = messages.length > 0;

  return (
    <section className={`agent-workspace ${hasMessages ? "conversation-active" : ""}`}>
      {!hasMessages && (
        <div className="workspace-intro">
          <div className="hero-badge">
            <Sparkles size={14} />
            <span>AI Agent Workspace</span>
          </div>

          <h1>
            Build with your
            <br />
            <span>intelligent agent.</span>
          </h1>

          <p>
            Interact with your MCP tools through a single intelligent
            workspace.
          </p>
        </div>
      )}

      <ChatWindow messages={messages} isLoading={isLoading} />

      {!hasMessages && (
        <div className="suggested-actions">
          <button
            onClick={() =>
              sendMessage(
                "Create a user named Ali with email ali@gmail.com"
              )
            }
          >
            <Users size={17} />

            <div>
              <strong>Create a user</strong>
              <span>Add a new user</span>
            </div>
          </button>

          <button onClick={() => sendMessage("Find user with ID 1")}>
            <Search size={17} />

            <div>
              <strong>Find a user</strong>
              <span>Search by ID</span>
            </div>
          </button>

          <button onClick={() => sendMessage("List all users")}>
            <Database size={17} />

            <div>
              <strong>List users</strong>
              <span>View your users</span>
            </div>
          </button>
        </div>
      )}

      <ChatInput onSend={sendMessage} />

      <div className="workspace-status">
        <Activity size={13} />
        <span>Agent ready</span>
        <span className="status-divider" />
        <span>5 MCP tools available</span>
      </div>
    </section>
  );
}

export default Dashboard;
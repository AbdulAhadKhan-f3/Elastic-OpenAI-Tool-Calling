import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";

function MessageBubble({ role, content }) {
  const isUser = role === "user";

  return (
    <div className={`message-row ${isUser ? "user-message" : "agent-message"}`}>
      <div className="message-avatar">
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>

      <div className="message-content">
        <div className="message-author">
          {isUser ? "You" : "Nexus"}
        </div>

        <div className="message-text">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}

export default MessageBubble;
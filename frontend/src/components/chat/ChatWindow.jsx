import { Bot, LoaderCircle, Sparkles } from "lucide-react";
import MessageBubble from "./MessageBubble";
import ToolExecution from "./ToolExecution";

function ChatWindow({ messages, isLoading }) {
  return (
    <div className="chat-window">
      {messages.length === 0 ? (
        <div className="chat-empty">
          <div className="empty-icon">
            <Sparkles size={22} />
          </div>

          <h2>How can I help?</h2>

        </div>
      ) : (
        <div className="messages">
          {messages.map((message) => {
            if (message.type === "tool") {
              return (
                <ToolExecution
                  key={message.id}
                  tool={message.tool}
                  arguments={message.arguments}
                  result={message.result}
                  status={message.status}
                  duration={message.duration}
                />
              );
            }

            return (
              <MessageBubble
                key={message.id}
                role={message.role}
                content={message.content}
              />
            );
          })}

          {isLoading && (
            <div className="message-row agent-message agent-thinking" role="status" aria-label="Agent is thinking">
              <div className="message-avatar">
                <Bot size={16} />
              </div>

              <div className="message-content">
                <div className="message-author">Nexus</div>
                <div className="thinking-indicator">
                  <LoaderCircle className="spin" size={14} />
                  <span>Working on it</span>
                  <span className="thinking-dots" aria-hidden="true">
                    <i />
                    <i />
                    <i />
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      
    </div>
  );
}

export default ChatWindow;
import { ArrowUp, Paperclip } from "lucide-react";
import { useState } from "react";

function ChatInput({ onSend }) {
  const [message, setMessage] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage) return;

    onSend(trimmedMessage);
    setMessage("");
  };

  return (
    <div className="chat-input-wrapper">
      <form className="chat-input" onSubmit={handleSubmit}>
        <textarea
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Ask your agent anything..."
          rows={1}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              handleSubmit(event);
            }
          }}
        />

        <div className="chat-input-footer">
          <button
            type="button"
            className="input-icon-button"
            aria-label="Attach file"
          >
            <Paperclip size={17} />
          </button>

          <button
            type="submit"
            className="send-button"
            disabled={!message.trim()}
            aria-label="Send message"
          >
            <ArrowUp size={18} />
          </button>
        </div>
      </form>

      <p className="input-disclaimer">
        Nexus can make mistakes. Tool executions are shown for transparency.
      </p>
    </div>
  );
}

export default ChatInput;
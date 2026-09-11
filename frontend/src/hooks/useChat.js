import { useState } from "react";
import { sendChatMessage } from "../services/api";

function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (content) => {
    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content,
    };

    setMessages((current) => [...current, userMessage]);
    setIsLoading(true);

    try {
      const { reply, tool_calls } = await sendChatMessage(content);

      // Each tool call becomes its own message, type: "tool",
      // exactly what ChatWindow.jsx checks for.
      const toolMessages = (tool_calls || []).map((call) => ({
        id: crypto.randomUUID(),
        type: "tool",
        tool: call.tool,
        arguments: call.arguments,
        result: call.result,
        status: call.status,
        duration: call.duration,
      }));

      const agentMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: reply,
      };

      // Tool cards appear first, then the final text reply below them —
      // matches your original mockup (tool card, then "User Ali was created successfully.")
      setMessages((current) => [...current, ...toolMessages, agentMessage]);
    } catch (err) {
      const errorMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: "Something went wrong reaching the agent. Is the backend running?",
      };

      setMessages((current) => [...current, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    messages,
    sendMessage,
    isLoading,
  };
}

export default useChat;
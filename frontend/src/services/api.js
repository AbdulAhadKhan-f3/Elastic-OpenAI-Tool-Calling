const API_BASE = "http://localhost:8001";

export async function sendChatMessage(message) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    throw new Error(`Chat request failed: ${res.status}`);
  }

  return res.json(); // { reply, tool_calls: [{ tool, arguments, result, duration, status }] }
}

export async function fetchMcpTools() {
  const res = await fetch(`${API_BASE}/api/tools`);

  if (!res.ok) {
    throw new Error(`Tool request failed: ${res.status}`);
  }

  return res.json();
}
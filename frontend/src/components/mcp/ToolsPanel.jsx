import { AlertCircle, LoaderCircle, Wrench } from "lucide-react";
import { useEffect, useState } from "react";
import { fetchMcpTools } from "../../services/api";
import ToolCard from "./ToolCard";

function ToolsPanel() {
	const [tools, setTools] = useState([]);
	const [isLoading, setIsLoading] = useState(true);
	const [error, setError] = useState("");

	useEffect(() => {
		let isCurrent = true;

		fetchMcpTools()
			.then(({ tools: availableTools }) => {
				if (isCurrent) setTools(availableTools || []);
			})
			.catch(() => {
				if (isCurrent) setError("Could not load tools from the backend.");
			})
			.finally(() => {
				if (isCurrent) setIsLoading(false);
			});

		return () => {
			isCurrent = false;
		};
	}, []);

	return (
		<section className="tools-panel">
			<div className="tools-heading">
				<div className="tools-heading-icon"><Wrench size={20} /></div>
				<div>
					<p className="eyebrow">MCP SERVER</p>
					<h1>Available tools</h1>
					<p>Tools currently exposed to the OpenAI agent.</p>
				</div>
			</div>

			{isLoading && (
				<div className="tools-state"><LoaderCircle className="spin" size={18} /> Loading tools...</div>
			)}

			{error && (
				<div className="tools-state tools-state-error"><AlertCircle size={18} /> {error}</div>
			)}

			{!isLoading && !error && (
				<div className="tools-grid">
					{tools.map((tool) => <ToolCard key={tool.name} tool={tool} />)}
				</div>
			)}
		</section>
	);
}

export default ToolsPanel;

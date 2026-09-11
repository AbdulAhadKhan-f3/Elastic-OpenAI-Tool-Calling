import {  Wrench } from "lucide-react";

function ToolCard({ tool }) {
	return (
		<article className="available-tool-card">
			<div className="available-tool-header">
				<div className="available-tool-icon"><Wrench size={16} /></div>
				<div>
					<p className="eyebrow">MCP TOOL</p>
					<h2>{tool.name}</h2>
				</div>
			</div>

			<p className="available-tool-description">
				{tool.description || "No description provided."}
			</p>

			{/* <div className="schema-heading"><Braces size={14} /> Input schema</div>
			<pre>{JSON.stringify(tool.parameters || {}, null, 2)}</pre> */}
		</article>	
	);
}

export default ToolCard;

import {
  Check,
  ChevronDown,
  Clock3,
  LoaderCircle,
  Wrench,
  X,
} from "lucide-react";

function ToolExecution({
  tool,
  arguments: toolArguments,
  result,
  status = "completed",
  duration,
}) {
  const isRunning = status === "running";
  const isError = status === "error";

  return (
    <div className={`tool-execution ${isError ? "tool-error" : ""}`}>
      <div className="tool-header">
        <div className="tool-title">
          <div className="tool-icon">
            {isRunning ? (
              <LoaderCircle className="spin" size={16} />
            ) : (
              <Wrench size={16} />
            )}
          </div>

          <div>
            <span className="tool-label">MCP TOOL</span>
            <strong>{tool}</strong>
          </div>
        </div>

        <div className="tool-status">
          {isRunning ? (
            <>
              <LoaderCircle className="spin" size={14} />
              <span>Running</span>
            </>
          ) : isError ? (
            <>
              <X size={14} />
              <span>Failed</span>
            </>
          ) : (
            <>
              <Check size={14} />
              <span>Completed</span>
            </>
          )}
        </div>
      </div>

      <div className="tool-body">
        <div className="tool-section">
          <div className="tool-section-header">
            <span>Arguments</span>
            <ChevronDown size={14} />
          </div>

          <pre>{JSON.stringify(toolArguments, null, 2)}</pre>
        </div>

        {result && (
          <div className="tool-section">
            <div className="tool-section-header">
              <span>Result</span>
            </div>

            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </div>

      {!isRunning && (
        <div className="tool-footer">
          <span>
            <Clock3 size={13} />
            {duration || "142"}ms
          </span>

          <span>MCP Server</span>
        </div>
      )}
    </div>
  );
}

export default ToolExecution;
import sys, json
from client import ManusAutonomousSandboxExecutor

def handle_mcp():
    manus = ManusAutonomousSandboxExecutor()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(manus.run_manus_benchmark(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-manus-autonomous-generalist-sandbox-executor-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "decompose_goal", "description": "Decompose human objective into autonomous plan.", "inputSchema": {"type": "object", "properties": {"goal": {"type": "string"}, "budget_usd": {"type": "number"}}}},
                    {"name": "execute_sandbox_step", "description": "Execute sandbox action step.", "inputSchema": {"type": "object", "properties": {"phase_id": {"type": "string"}, "action_type": {"type": "string"}}}},
                    {"name": "run_manus_benchmark", "description": "Run Manus generalist agent benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "decompose_goal":
                    res = manus.decompose_goal(args.get("goal", ""), args.get("budget_usd"))
                elif tname == "execute_sandbox_step":
                    res = manus.execute_sandbox_step(args.get("phase_id", "p1"), args.get("action_type", "BROWSE_SEARCH"), args.get("payload", {}))
                else:
                    res = manus.run_manus_benchmark()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()

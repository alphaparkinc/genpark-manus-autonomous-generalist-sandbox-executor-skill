from client import ManusAutonomousSandboxExecutor
import json

manus = ManusAutonomousSandboxExecutor()
print("=== MANUS AUTONOMOUS GENERALIST EXECUTOR BENCHMARK ===")
res = manus.run_manus_benchmark()
print(json.dumps(res, indent=2))

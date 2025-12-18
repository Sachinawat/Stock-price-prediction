from pathlib import Path

PROJECT_NAME = "Fast-MCP-Stock-Agent"

structure = [
    "clients/__init__.py",
    "clients/client.py",

    "servers/__init__.py",
    "servers/mcp_server.py",

    "servers/tools/__init__.py",
    "servers/tools/market_data.py",
    "servers/tools/features.py",
    "servers/tools/machine_learning.py",
    "servers/tools/utils.py",

    "data/.gitkeep",          # keeps empty folder in git
    "requirements.txt",
    "README.md",
]

base = Path(PROJECT_NAME)

for item in structure:
    path = base / item
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

print(f"✅ Project '{PROJECT_NAME}' created successfully")

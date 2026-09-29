import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent
PILOT_DIR = TOOLS_DIR.parent
REPO_DIR = PILOT_DIR.parent.parent
for p in (TOOLS_DIR, REPO_DIR / "probe"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

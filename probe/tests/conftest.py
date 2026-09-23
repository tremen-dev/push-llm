import sys
from pathlib import Path

PROBE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = PROBE_DIR.parent
if str(PROBE_DIR) not in sys.path:
    sys.path.insert(0, str(PROBE_DIR))

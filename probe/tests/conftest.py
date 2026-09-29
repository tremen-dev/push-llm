import sys
from pathlib import Path

PROBE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = PROBE_DIR.parent
if str(PROBE_DIR) not in sys.path:
    sys.path.insert(0, str(PROBE_DIR))


import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _never_read_the_real_dotenv(tmp_path_factory, monkeypatch):
    """F-SPEC-002-1: no test may read the repo-root .env (real keys, ADR-006)."""
    import run_probe
    fake = tmp_path_factory.mktemp("no-dotenv") / ".env"
    if hasattr(run_probe, "DOTENV_PATH"):
        monkeypatch.setattr(run_probe, "DOTENV_PATH", fake)

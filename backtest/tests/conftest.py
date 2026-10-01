"""Make ``fqe_backtest`` importable without ``pip install -e .``."""

import sys
from pathlib import Path

BACKTEST_DIR = Path(__file__).resolve().parents[1]
if str(BACKTEST_DIR) not in sys.path:
    sys.path.insert(0, str(BACKTEST_DIR))


from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

APP_NAME = "Intelligence Kernel"
VERSION = "0.8.0"

MEMORY_DIR = ROOT / "memory"
MEMORY_FILE = MEMORY_DIR / "memory.json"

LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "kernel.log"

LOG_LEVEL = "INFO"


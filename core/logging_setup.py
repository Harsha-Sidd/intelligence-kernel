
import logging
from pathlib import Path

from core.config import LOG_FILE, LOG_LEVEL


def configure_logging(log_file=LOG_FILE, level=LOG_LEVEL):
    """Configure a private, local diagnostic log."""

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("intelligence_kernel")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False

    # Replace existing handlers to avoid duplicate log entries.
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    file_handler = logging.FileHandler(
        log_path,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


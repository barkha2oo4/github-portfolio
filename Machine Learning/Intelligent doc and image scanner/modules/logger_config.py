import logging
import os
from datetime import datetime


def setup_logger(log_level=logging.INFO, logs_dir: str = "results/logs") -> logging.Logger:
    """Create and return a configured logger instance.

    Args:
        log_level: logging level (default INFO)
        logs_dir: directory to store log files

    Returns:
        logging.Logger: configured logger named 'IDIS'
    """
    os.makedirs(logs_dir, exist_ok=True)

    logger = logging.getLogger("IDIS")
    logger.setLevel(log_level)

    # avoid adding handlers multiple times in interactive runs
    if logger.handlers:
        return logger

    # File handler with timestamped filename
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    file_path = os.path.join(logs_dir, filename)
    fh = logging.FileHandler(file_path, encoding="utf-8")
    fh.setLevel(log_level)
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)d | %(message)s"))

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)8s | %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("✅ Logging system initialized.")
    return logger


__all__ = ["setup_logger"]

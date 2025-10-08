import logging
import sys
from typing import Optional


def get_logger(name: str = "api_tests", level: int = logging.INFO, stream: Optional[logging.StreamHandler] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = stream or logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger

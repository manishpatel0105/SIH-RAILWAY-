"""
Structured Logging Configuration
=================================

Sets up Python's logging module to output structured, consistent logs.

WHY structured logging?
  - Every log line has the same format → easier to grep/filter
  - Timestamps are always present → essential for debugging async code
  - Module name is included → you know exactly where the log came from
  - In production, you can switch to JSON format for log aggregation tools

USAGE:
  Import and call `setup_logging()` once at app startup (in main.py).
  Then use standard logging in any module:

      import logging
      logger = logging.getLogger(__name__)
      logger.info("Block plan optimized", extra={"plan_id": 42})
"""

import logging
import sys


def setup_logging(*, debug: bool = False) -> None:
    """
    Configure the root logger with a consistent format.

    Args:
        debug: If True, set log level to DEBUG. Otherwise, INFO.
    """
    log_level = logging.DEBUG if debug else logging.INFO

    # Define a format that includes all the context we need
    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
    )

    # Configure the root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
        # force=True replaces any existing handlers (prevents duplicates)
        force=True,
    )

    # Quiet down noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if debug else logging.WARNING
    )

    logging.getLogger(__name__).info(
        "Logging configured — level=%s", logging.getLevelName(log_level)
    )

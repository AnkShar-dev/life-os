"""Logging setup helpers."""

import logging


def setup_logging(level: str = "INFO") -> None:
    """Configure application-wide logging."""

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

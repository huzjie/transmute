# -*- coding: utf-8 -*-
"""统一日志：标准库 logging 薄封装。"""
from __future__ import annotations

import logging
import os

_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def get_logger(name: str = "transmute") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter(_FMT))
        logger.addHandler(h)
        logger.setLevel(os.environ.get("TM_LOG_LEVEL", "INFO"))
        logger.propagate = False
    return logger

# -*- coding: utf-8 -*-
"""transmute — 多智能体验证式代码迁移编排引擎。"""
from __future__ import annotations

__version__ = "0.1.0"

from ._core import RNG, seed_from
from .config import Config, load_config

__all__ = ["__version__", "RNG", "seed_from", "Config", "load_config"]

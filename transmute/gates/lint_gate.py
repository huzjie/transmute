# -*- coding: utf-8 -*-
"""静态检查门禁：clippy / ruff 之类。"""
from .base import Gate


class LintGate(Gate):
    name = "lint"

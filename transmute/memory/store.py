# -*- coding: utf-8 -*-
"""MemoryStore：磁盘持久化工作记忆（JSON），跨子任务、跨运行可恢复。"""
from __future__ import annotations

import json
import os
from pathlib import Path


class MemoryStore:
    """把上下文/状态落到 JSON 文件，支持断点续跑。"""

    def __init__(self, path: str = ".transmute/memory.json"):
        self.path = Path(path)
        self._data: dict = {}

    def load(self) -> dict:
        if self.path.exists():
            try:
                self._data = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self._data = {}
        return self._data

    def save(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        self._data = data

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        self._data[key] = value
        self.save(self._data)

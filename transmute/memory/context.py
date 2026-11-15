# -*- coding: utf-8 -*-
"""MigrationContext：一次迁移的共享上下文（项目路径、计划、已合并符号表）。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class MigrationContext:
    root: str = "."
    source_lang: str = "cpp"
    target_lang: str = "rust"
    merged_symbols: Set[str] = field(default_factory=set)   # 已迁移完成的符号
    notes: List[str] = field(default_factory=list)          # 累积的全局说明
    stats: Dict[str, int] = field(default_factory=lambda: {
        "generated": 0, "passed": 0, "reviewed": 0, "merged": 0, "rejected": 0,
    })

    def mark_merged(self, symbols: List[str]) -> None:
        self.merged_symbols.update(symbols)

    def add_note(self, note: str) -> None:
        if note not in self.notes:
            self.notes.append(note)

    def snapshot(self) -> dict:
        return {
            "merged_symbols": sorted(self.merged_symbols),
            "notes": list(self.notes),
            "stats": dict(self.stats),
        }

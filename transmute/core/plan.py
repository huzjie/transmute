# -*- coding: utf-8 -*-
"""MigrationPlan：整个迁移的切分结果 + 序列化。"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from .task import Subtask, Status


@dataclass
class MigrationPlan:
    source_lang: str = "cpp"
    target_lang: str = "rust"
    root: str = "."
    tasks: List[Subtask] = field(default_factory=list)

    def by_id(self, tid: str) -> Subtask:
        for t in self.tasks:
            if t.id == tid:
                return t
        raise KeyError(tid)

    def pending(self) -> List[Subtask]:
        return [t for t in self.tasks if t.status == Status.PENDING]

    def done_count(self) -> int:
        return sum(1 for t in self.tasks if t.status in (Status.MERGED, Status.REVIEWED))

    def summary(self) -> dict:
        return {
            "total": len(self.tasks),
            "done": self.done_count(),
            "pending": len(self.pending()),
            "failed": sum(1 for t in self.tasks if t.status == Status.FAILED),
        }

    def to_json(self) -> str:
        return json.dumps({
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "root": self.root,
            "tasks": [t.to_dict() for t in self.tasks],
        }, ensure_ascii=False, indent=2)

    def save(self, path: str) -> None:
        Path(path).write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, path: str) -> "MigrationPlan":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        plan = cls(
            source_lang=data.get("source_lang", "cpp"),
            target_lang=data.get("target_lang", "rust"),
            root=data.get("root", "."),
        )
        plan.tasks = [Subtask.from_dict(t) for t in data.get("tasks", [])]
        return plan

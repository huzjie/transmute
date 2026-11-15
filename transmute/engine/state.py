# -*- coding: utf-8 -*-
"""RunState：一次迁移运行的进度状态（可序列化，支持断点续跑）。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class RunState:
    plan_path: str = ""
    started_at: str = ""
    finished_at: str = ""
    results: Dict[str, dict] = field(default_factory=dict)   # task_id -> 结果
    errors: List[str] = field(default_factory=list)

    def record(self, task_id: str, status: str, detail: str = "") -> None:
        self.results[task_id] = {"status": status, "detail": detail}

    def to_dict(self) -> dict:
        return {
            "plan_path": self.plan_path,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "results": self.results,
            "errors": self.errors,
        }

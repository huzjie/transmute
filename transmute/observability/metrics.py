# -*- coding: utf-8 -*-
"""指标：迁移过程计数（生成/通过/复核/合并/拒绝）。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Metrics:
    generated: int = 0
    passed: int = 0
    reviewed: int = 0
    merged: int = 0
    rejected: int = 0
    duration_ms: int = 0

    def record(self, event: str) -> None:
        if event in self.__dict__:
            self.__dict__[event] += 1

    def to_dict(self) -> dict:
        return {
            "generated": self.generated, "passed": self.passed,
            "reviewed": self.reviewed, "merged": self.merged,
            "rejected": self.rejected, "duration_ms": self.duration_ms,
        }

# -*- coding: utf-8 -*-
"""轻量追踪：嵌套 Span，记录每个子任务的耗时。"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List


@dataclass
class Span:
    name: str
    start_ms: int = 0
    duration_ms: int = 0
    children: List["Span"] = field(default_factory=list)

    def __enter__(self):
        self.start_ms = int(time.time() * 1000)
        return self

    def __exit__(self, *exc):
        self.duration_ms = int(time.time() * 1000) - self.start_ms


class _Tracer:
    def __init__(self):
        self.root: List[Span] = []

    def span(self, name: str) -> Span:
        s = Span(name=name)
        self.root.append(s)
        return s


tracer = _Tracer()

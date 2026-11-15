# -*- coding: utf-8 -*-
"""依赖图：DAG 构建 + 拓扑分批（同一批内无相互依赖，可并行）。"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, List, Sequence

from ..task import Subtask


class DependencyGraph:
    """把一组 Subtask 按 depends_on 构建 DAG，并给出拓扑排序批次。"""

    def __init__(self, tasks: Sequence[Subtask]):
        self.tasks = {t.id: t for t in tasks}
        # 邻接表：tid -> 依赖它的后续任务
        self.dependents: Dict[str, List[str]] = defaultdict(list)
        self.indegree: Dict[str, int] = {t.id: 0 for t in tasks}
        for t in tasks:
            for dep in t.depends_on:
                if dep in self.tasks:
                    self.dependents[dep].append(t.id)
                    self.indegree[t.id] += 1

    def has_cycle(self) -> bool:
        return sum(1 for _ in self._kahn()) != len(self.tasks)

    def _kahn(self):
        indeg = dict(self.indegree)
        q = deque([tid for tid, d in indeg.items() if d == 0])
        while q:
            tid = q.popleft()
            yield tid
            for nxt in self.dependents.get(tid, []):
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    q.append(nxt)

    def topological_order(self) -> List[str]:
        return list(self._kahn())

    def batches(self, limit: int | None = None) -> List[List[str]]:
        """拓扑分批：每批内部无相互依赖，可并行；limit 限制每批最大数量。"""
        indeg = dict(self.indegree)
        ready = deque(sorted(tid for tid, d in indeg.items() if d == 0))
        result: List[List[str]] = []
        while ready:
            batch = []
            next_ready = deque()
            while ready and (limit is None or len(batch) < limit):
                batch.append(ready.popleft())
            for tid in batch:
                for nxt in self.dependents.get(tid, []):
                    indeg[nxt] -= 1
                    if indeg[nxt] == 0:
                        next_ready.append(nxt)
            result.append(batch)
            # 合并下一轮就绪的任务到 ready（保持稳定顺序）
            while next_ready:
                ready.append(next_ready.popleft())
        return result


def topological_batches(tasks: Sequence[Subtask], limit: int | None = None) -> List[List[str]]:
    return DependencyGraph(tasks).batches(limit)

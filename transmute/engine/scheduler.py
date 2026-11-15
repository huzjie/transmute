# -*- coding: utf-8 -*-
"""Scheduler：按依赖图拓扑分批，批内并行、批间顺序。"""
from __future__ import annotations

import concurrent.futures
from typing import Callable, List

from ..core.dependency.graph import topological_batches
from ..core.task import Subtask


def run_scheduled(tasks: List[Subtask], worker: Callable[[Subtask], dict], max_parallel: int = 4) -> dict:
    """拓扑分批调度：同批并行，逐批执行 worker，汇总结果。"""
    batches = topological_batches(tasks, limit=max_parallel)
    results: dict = {}
    for batch in batches:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_parallel) as ex:
            futures = {ex.submit(worker, t): t.id for t in _by_id(tasks, batch)}
            for fut in concurrent.futures.as_completed(futures):
                tid = futures[fut]
                try:
                    results[tid] = fut.result()
                except Exception as e:  # noqa: BLE001
                    results[tid] = {"status": "failed", "detail": str(e)}
    return results


def _by_id(tasks: List[Subtask], ids: List[str]) -> List[Subtask]:
    m = {t.id: t for t in tasks}
    return [m[i] for i in ids if i in m]

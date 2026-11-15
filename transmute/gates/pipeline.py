# -*- coding: utf-8 -*-
"""GatePipeline：把多道门禁串成「任何一关不过即失败」的管线。"""
from __future__ import annotations

from typing import List

from .base import Gate, GateResult


class GatePipeline:
    """按顺序跑门禁；第一个失败即短路（默认 stop_on_fail）。"""

    def __init__(self, gates: List[Gate], stop_on_fail: bool = True):
        self.gates = gates
        self.stop_on_fail = stop_on_fail

    def run(self) -> List[GateResult]:
        results: List[GateResult] = []
        for g in self.gates:
            r = g.run()
            results.append(r)
            if self.stop_on_fail and not r.passed:
                break
        return results

    def all_passed(self, results: List[GateResult]) -> bool:
        return bool(results) and all(r.passed for r in results)

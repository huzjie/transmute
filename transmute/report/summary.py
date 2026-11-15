# -*- coding: utf-8 -*-
"""汇总：从 MigrationPlan 生成结构化摘要。"""
from __future__ import annotations

from ..core.plan import MigrationPlan
from ..core.task import Status


def build_summary(plan: MigrationPlan) -> dict:
    """生成迁移摘要：总数/成功/失败 + 每个子任务的状态。"""
    rows = []
    for t in plan.tasks:
        rows.append({
            "id": t.id,
            "target": t.target,
            "status": t.status.value,
            "retries": t.retries,
            "report": (t.report or "")[:120],
        })
    by_status = {}
    for t in plan.tasks:
        by_status[t.status.value] = by_status.get(t.status.value, 0) + 1
    return {
        "source_lang": plan.source_lang,
        "target_lang": plan.target_lang,
        "total": len(plan.tasks),
        "by_status": by_status,
        "tasks": rows,
    }

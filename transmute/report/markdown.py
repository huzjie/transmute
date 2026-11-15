# -*- coding: utf-8 -*-
"""Markdown 报告。"""
from __future__ import annotations

from ..core.plan import MigrationPlan


def to_markdown(plan: MigrationPlan) -> str:
    lines = [f"# 迁移报告（{plan.source_lang} → {plan.target_lang}）", ""]
    lines.append("| ID | 目标 | 状态 | 重试 | 说明 |")
    lines.append("|---|---|---|---|---|")
    for t in plan.tasks:
        lines.append(f"| {t.id} | {t.target} | {t.status.value} | {t.retries} | "
                     f"{(t.report or '').replace(chr(10), ' ')[:80]} |")
    return "\n".join(lines)

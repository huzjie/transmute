# -*- coding: utf-8 -*-
"""HTML 报告（自包含，可直接打开）。"""
from __future__ import annotations

from ..core.plan import MigrationPlan

_STATUS_COLOR = {
    "merged": "#28a745", "reviewed": "#17a2b8", "passed": "#ffc107",
    "rejected": "#dc3545", "failed": "#dc3545", "pending": "#6c757d",
}


def to_html(plan: MigrationPlan) -> str:
    rows = []
    for t in plan.tasks:
        color = _STATUS_COLOR.get(t.status.value, "#6c757d")
        rows.append(
            f"<tr><td>{t.id}</td><td>{t.target}</td>"
            f'<td style="color:{color};font-weight:600">{t.status.value}</td>'
            f"<td>{t.retries}</td><td>{(t.report or '')[:100]}</td></tr>"
        )
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>迁移报告</title>
<style>body{{font-family:'Microsoft YaHei',sans-serif;padding:24px;color:#1f2329}}
table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #e5e6eb;padding:8px 12px;text-align:left}}
th{{background:#f5f6f8}}</style></head>
<body><h2>迁移报告（{plan.source_lang} → {plan.target_lang}）</h2>
<table><tr><th>ID</th><th>目标</th><th>状态</th><th>重试</th><th>说明</th></tr>
{''.join(rows)}</table></body></html>"""

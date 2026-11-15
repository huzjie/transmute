# -*- coding: utf-8 -*-
"""CSV 导出。"""
from __future__ import annotations

import csv
import io

from ..core.plan import MigrationPlan


def to_csv(plan: MigrationPlan) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id", "target", "status", "retries", "report"])
    for t in plan.tasks:
        w.writerow([t.id, t.target, t.status.value, t.retries, t.report])
    return buf.getvalue()

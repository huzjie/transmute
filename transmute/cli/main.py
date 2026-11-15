# -*- coding: utf-8 -*-
"""transmute 命令行入口。"""
from __future__ import annotations

import argparse
import sys


def _cmd_doctor(args) -> int:
    from .doctor import run_doctor
    ok = run_doctor()
    return 0 if ok else 1


def _cmd_plan(args) -> int:
    from ..config import load_config
    from ..engine.orchestrator import Orchestrator
    cfg = load_config(args.config)
    plan = Orchestrator(config=cfg).build_plan()
    plan.save(cfg.plan_file)
    print(f"✅ 迁移计划已生成: {cfg.plan_file}（{len(plan.tasks)} 个子任务）")
    for t in plan.tasks[:10]:
        print(f"  - {t.id}  {t.target}")
    if len(plan.tasks) > 10:
        print(f"  ...（其余 {len(plan.tasks) - 10} 个）")
    return 0


def _cmd_run(args) -> int:
    from ..config import load_config
    from ..engine.orchestrator import Orchestrator
    cfg = load_config(args.config)
    result = Orchestrator(config=cfg).run()
    summary = result["summary"]
    print(f"✅ 迁移完成: 共 {summary['total']} 个，成功 {summary['done']} 个，"
          f"待处理 {summary['pending']} 个，失败 {summary['failed']} 个")
    return 0


def _cmd_status(args) -> int:
    import json
    from pathlib import Path
    from ..core.plan import MigrationPlan
    p = Path(args.plan)
    if not p.exists():
        print("⚠️ 未找到计划文件，请先 `transmute plan`")
        return 1
    plan = MigrationPlan.load(args.plan)
    print(json.dumps(plan.summary(), ensure_ascii=False, indent=2))
    for t in plan.tasks:
        mark = {"merged": "✅", "reviewed": "✅", "passed": "🟡"}.get(t.status.value, "⬜")
        print(f"  {mark} {t.id}  {t.target}  [{t.status.value}]")
    return 0


def _cmd_report(args) -> int:
    from pathlib import Path
    from ..core.plan import MigrationPlan
    p = Path(args.plan)
    if not p.exists():
        print("⚠️ 未找到计划文件")
        return 1
    plan = MigrationPlan.load(args.plan)
    fails = [t for t in plan.tasks if t.status.value in ("rejected", "failed")]
    print(f"失败子任务 {len(fails)} 个：")
    for t in fails:
        print(f"  ❌ {t.id}  {t.target}")
        print(f"     {t.report[:200]}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="transmute", description="多智能体验证式代码迁移编排引擎")
    sub = p.add_subparsers(dest="cmd")

    sp_plan = sub.add_parser("plan", help="生成迁移计划（按依赖图切分）")
    sp_plan.add_argument("--config", default="config.yaml")
    sp_plan.set_defaults(func=_cmd_plan)

    sp_doc = sub.add_parser("doctor", help="自检 9 项")
    sp_doc.set_defaults(func=_cmd_doctor)

    sp_run = sub.add_parser("run", help="跑完整迁移")
    sp_run.add_argument("--config", default="config.yaml")
    sp_run.set_defaults(func=_cmd_run)

    sp_st = sub.add_parser("status", help="查看迁移进度")
    sp_st.add_argument("--plan", default="migration.plan.json")
    sp_st.set_defaults(func=_cmd_status)

    sp_rp = sub.add_parser("report", help="输出失败子任务报告")
    sp_rp.add_argument("--plan", default="migration.plan.json")
    sp_rp.set_defaults(func=_cmd_report)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "cmd", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

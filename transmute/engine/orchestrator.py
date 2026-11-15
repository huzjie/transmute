# -*- coding: utf-8 -*-
"""Orchestrator：把切分/生成/门禁/复核/合并串成端到端迁移。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..agents.generator import GeneratorAgent
from ..agents.reviewer import ReviewerAgent
from ..core.decompose import DecomposeOptions, decompose, enrich_read_scope
from ..core.plan import MigrationPlan
from ..core.task import Subtask, Status
from ..gates.compile_gate import CompileGate
from ..gates.lint_gate import LintGate
from ..gates.pipeline import GatePipeline
from ..gates.test_gate import TestGate
from ..llm.registry import get_provider
from ..memory.context import MigrationContext
from ..scopes.filescope import FileScope
from ..scopes.sandbox import Sandbox
from ..scopes.toolscope import ToolScope
from .state import RunState


@dataclass
class Orchestrator:
    config: object
    plan: Optional[MigrationPlan] = None
    state: RunState = field(default_factory=RunState)

    def make_provider(self, model):
        cfg = self.config
        return get_provider(
            cfg.llm_provider, model=model, temperature=cfg.llm_temperature,
            api_key=cfg.api_key(), base_url=cfg.llm_base_url,
        )

    def build_plan(self) -> MigrationPlan:
        opts = DecomposeOptions(
            root=self.config.migration_root,
            source_lang=self.config.source_lang,
            target_lang=self.config.target_lang,
        )
        plan = decompose(opts)
        plan = enrich_read_scope(plan, self.config.migration_root)
        self.plan = plan
        return plan

    def _pipeline(self) -> GatePipeline:
        cfg = self.config
        return GatePipeline([
            CompileGate(cfg.compile_cmd, cfg.compile_timeout, cfg.migration_root),
            TestGate(cfg.test_cmd, cfg.test_timeout, cfg.migration_root),
            LintGate(cfg.lint_cmd, cfg.lint_timeout, cfg.migration_root),
        ])

    def run_one(self, task: Subtask) -> dict:
        """跑单个子任务：生成候选 → 门禁 → 复核，返回结构化结果。"""
        ctx = MigrationContext(root=self.config.migration_root)
        generator = GeneratorAgent(
            self.make_provider(self.config.generator_model),
            source_lang=self.config.source_lang, target_lang=self.config.target_lang,
        )
        reviewer = ReviewerAgent(
            self.make_provider(self.config.reviewer_model),
            source_lang=self.config.source_lang, target_lang=self.config.target_lang,
            strictness=self.config.reviewer_strictness,
        )
        file_scope = FileScope(
            root=self.config.migration_root,
            read_scope=[task.source_file] + task.read_scope,
            write_scope=[task.dest_file],
        )
        sandbox = Sandbox(
            file_scope=file_scope,
            tool_scope=ToolScope(task.tool_scope),
            allow_network=self.config.allow_network,
            read_only_outside_target=self.config.read_only_outside_target,
        )

        # 1. 读取源文件
        src = sandbox.read_file(task.source_file)
        if not src.get("ok"):
            return {"status": "failed", "detail": src.get("error", "读取源文件失败")}

        # 2. 生成候选
        candidate = generator.run(
            source_file=task.source_file, dest_file=task.dest_file,
            read_scope=[task.source_file] + task.read_scope,
            tool_scope=task.tool_scope, acceptance=task.acceptance,
        )
        task.candidate = candidate

        # 3. 写候选到目标文件
        code = self._extract_code(candidate)
        w = sandbox.write_file(task.dest_file, code)
        if not w.get("ok"):
            return {"status": "rejected", "detail": w.get("error", "写入候选失败")}

        # 4. 门禁
        gate_results = self._pipeline().run()
        if not self._pipeline().all_passed(gate_results):
            brief = "；".join(r.brief() for r in gate_results)
            task.report = brief
            return {"status": "rejected", "detail": brief}

        # 5. 复核
        verdict = reviewer.run(
            source_file=task.source_file, dest_file=task.dest_file,
            source_code=src["content"], candidate=code,
        )
        accepted = "<accept>" in verdict and "<reject>" not in verdict
        if not accepted:
            task.report = verdict
            return {"status": "rejected", "detail": verdict}

        return {"status": "passed", "detail": "门禁 + 复核通过"}

    def run(self) -> dict:
        """端到端：切分 → 逐子任务迁移 → 汇总。"""
        if self.plan is None:
            self.plan = self.build_plan()
        plan = self.plan
        from .scheduler import run_scheduled
        from datetime import datetime
        self.state.started_at = datetime.now().isoformat()
        results = run_scheduled(plan.tasks, self.run_one, max_parallel=self.config.max_parallel)
        for tid, r in results.items():
            t = plan.by_id(tid)
            st = r.get("status", "failed")
            t.status = {
                "passed": Status.REVIEWED, "rejected": Status.REJECTED,
                "failed": Status.FAILED,
            }.get(st, Status.FAILED)
            t.report = r.get("detail", "")
            self.state.record(tid, st, t.report)
        self.state.finished_at = datetime.now().isoformat()
        if self.config.plan_file:
            plan.save(self.config.plan_file)
        return {"summary": plan.summary(), "state": self.state.to_dict()}

    @staticmethod
    def _extract_code(text: str) -> str:
        """从候选文本里抽代码块；没有代码块则整体返回。"""
        import re
        m = re.search(r"```[\\w]*\n(.*?)```", text, re.S)
        if m:
            return m.group(1)
        return text


def run_migration(config) -> dict:
    """便捷入口：给定 Config，跑一次完整迁移。"""
    orch = Orchestrator(config=config)
    return orch.run()

# -*- coding: utf-8 -*-
"""ReviewerAgent：只负责「挑错」，不写代码。与生成者职责分离。"""
from __future__ import annotations

from typing import List

from .base import Agent

REVIEW_CHECKLIST = [
    "语义等价：有没有漏函数、改控制流、改常量？",
    "内存安全：data race / use-after-free / 错误所有权转移？",
    "边界：整数溢出 / 索引越界 / null 处理是否对齐原语义？",
    "越界：是否改动或引用了 read_scope 之外的文件？",
    "风格：是否混入了无关重构？",
]

_SYSTEM = """你是 {source_lang}→{target_lang} 迁移的审校员。
你**不写代码**，只负责从候选里挑错。逐条核对以下清单：
{checklist}
任何一项不达标 → 输出 `<reject>` + 具体位置 + 修复建议；
全部达标才输出 `<accept>`。不确定算不达标，从严判。
"""


class ReviewerAgent(Agent):
    def __init__(self, provider, source_lang="cpp", target_lang="rust", strictness="high"):
        checklist = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(REVIEW_CHECKLIST))
        super().__init__(
            role="reviewer",
            provider=provider,
            system_prompt=_SYSTEM.format(
                source_lang=source_lang, target_lang=target_lang, checklist=checklist
            ),
        )
        self.strictness = strictness

    def build_prompt(self, source_file, dest_file, source_code, candidate, gate_report=""):
        gate = f"\n门禁结果：\n{gate_report}" if gate_report else ""
        return f"""请审校以下 {dest_file} 迁移候选（源文件 {source_file}）。

<source>
{source_code[:6000]}
</source>

<candidate>
{candidate[:6000]}
</candidate>
{gate}

只输出：`<accept>` 或 `<reject> + 位置 + 修复建议`。
"""

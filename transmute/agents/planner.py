# -*- coding: utf-8 -*-
"""PlannerAgent：可选，用 LLM 生成/优化迁移计划（默认用规则切分即可）。"""
from __future__ import annotations

from .base import Agent

_SYSTEM = """你是代码迁移规划师。给定一个待迁移代码库，输出切分建议：
把迁移按依赖关系切成细粒度子任务，每个子任务标注：
- target（源文件 -> 目标文件）
- read_scope（允许读取的上下文文件）
- acceptance（验收测试）
要求子任务粒度尽量小、相互依赖尽量少，方便并行与回滚。
"""


class PlannerAgent(Agent):
    def __init__(self, provider):
        super().__init__(role="planner", provider=provider, system_prompt=_SYSTEM)

    def build_prompt(self, source_lang, target_lang, file_list, max_files=200):
        files = "\n".join(f"- {f}" for f in file_list[:max_files])
        return f"""待迁移代码库（{source_lang} -> {target_lang}），源文件清单：
{files}

请给出迁移切分建议（JSON 列表，每项含 target/read_scope/acceptance 字段）。
"""

# -*- coding: utf-8 -*-
"""GeneratorAgent：只负责「读作用域内文件 → 产出候选迁移」。"""
from __future__ import annotations

from typing import List

from .base import Agent

_SYSTEM = """你是 {source_lang}→{target_lang} 迁移工程师。
你**只能**读取 <read_scope> 列出的文件、只能调用 <tool_scope> 列出的工具。
你的唯一产出是目标文件的完整 {target_lang} 重写，要求：
1. 语义等价：不新增/不删减任何行为，逐函数对齐原语义；
2. 内存安全：所有权、借用、生命周期写对，禁止 unsafe（除非有注释说明理由）；
3. 不做无关重构：不顺手改命名、不优化、不删注释；
4. 完成后调用 run_test 跑 <acceptance>，通过后再提交候选。
"""


class GeneratorAgent(Agent):
    def __init__(self, provider, source_lang="cpp", target_lang="rust"):
        super().__init__(
            role="generator",
            provider=provider,
            system_prompt=_SYSTEM.format(source_lang=source_lang, target_lang=target_lang),
        )

    def build_prompt(self, source_file, dest_file, read_scope, tool_scope, acceptance, context_summary=""):
        scope_txt = "\n".join(f"- {s}" for s in read_scope) or "- （无）"
        tools_txt = "、".join(tool_scope)
        accept_txt = "\n".join(f"- {a}" for a in acceptance) or "- （无）"
        ctx = f"\n已迁移的全局上下文：\n{context_summary}" if context_summary else ""
        return f"""目标：把 {source_file} 迁移为 {dest_file}

<read_scope>
{scope_txt}
</read_scope>

<tool_scope>
{tools_txt}
</tool_scope>

<acceptance>
{accept_txt}
</acceptance>
{ctx}

请先 read_file 读取 {source_file}（及作用域内的必要上下文），再产出 {dest_file} 的完整代码，
最后 run_test 验证 <acceptance>。输出格式：先输出代码块，再输出「<accept>」或「<reject> + 原因」。
"""

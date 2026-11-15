# -*- coding: utf-8 -*-
"""Agent 基类：把 LLM + 系统提示词 + 作用域绑定为一个可调用单元。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..llm.base import LLMProvider


@dataclass
class Agent:
    role: str
    provider: LLMProvider
    system_prompt: str = ""

    def build_prompt(self, **kw) -> str:
        """子类覆写：把结构化输入拼成最终 user prompt。"""
        raise NotImplementedError

    def run(self, **kw) -> str:
        prompt = self.build_prompt(**kw)
        result = self.provider.complete(prompt, system=self.system_prompt)
        return result.text

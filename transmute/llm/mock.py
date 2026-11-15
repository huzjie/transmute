# -*- coding: utf-8 -*-
"""Mock provider：无外部依赖，用于冒烟/单测/离线演示。"""
from __future__ import annotations

from .base import LLMProvider, LLMResult


class MockProvider(LLMProvider):
    """把输入 prompt 原样回显，便于在无 LLM 环境下跑通整条流水线。"""

    name = "mock"

    def complete(self, prompt, system=""):
        return LLMResult(text=f"[mock] {prompt}")

    def chat(self, messages, temperature=None):
        last = messages[-1].get("content", "") if messages else ""
        return LLMResult(text=f"[mock] {last}")


from .registry import register  # noqa: E402

register(MockProvider)

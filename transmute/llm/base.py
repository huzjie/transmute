# -*- coding: utf-8 -*-
"""LLM provider 抽象接口。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class LLMResult:
    text: str
    raw: Any = None
    usage: dict | None = None

    def __str__(self) -> str:
        return self.text


class LLMProvider:
    """统一 LLM 调用接口：complete(prompt, system)。"""

    name = "base"

    def __init__(self, model: str, temperature: float = 0.2, api_key: str = "", **kw):
        self.model = model
        self.temperature = temperature
        self.api_key = api_key
        self.extra = kw

    def complete(self, prompt: str, system: str = "") -> LLMResult:
        raise NotImplementedError

    def chat(self, messages: list, temperature: float | None = None) -> LLMResult:
        raise NotImplementedError

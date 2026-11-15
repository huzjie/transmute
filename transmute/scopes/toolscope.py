# -*- coding: utf-8 -*-
"""ToolScope：约束智能体只能调用白名单内的工具。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List

_DEFAULT_TOOLS = {"read_file", "write_file", "run_test", "git_branch"}


@dataclass
class ToolScope:
    allowed: List[str] = field(default_factory=lambda: sorted(_DEFAULT_TOOLS))

    def allow_tool(self, name: str) -> bool:
        return name in self.allowed

    def as_prompt(self) -> str:
        return "允许调用的工具：" + ", ".join(self.allowed)


def allow_tool(allowed: List[str], name: str) -> bool:
    return name in allowed

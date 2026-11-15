# -*- coding: utf-8 -*-
"""provider 注册表：存「实例」，惰性 import 内置模块触发注册。"""
from __future__ import annotations

from typing import Dict, List

from .base import LLMProvider

_REGISTRY: Dict[str, LLMProvider] = {}


def register(cls) -> None:
    """注册 provider 类（按 name）。"""
    _REGISTRY[cls.name] = cls


def list_providers() -> List[str]:
    """惰性 import 所有内置模块，确保注册表完整。"""
    from . import openai_compat, anthropic, mock  # noqa: F401
    return sorted(_REGISTRY.keys())


def get_provider(name: str, model: str = "mock", temperature: float = 0.2,
                 api_key: str = "", base_url: str = "", **kw) -> LLMProvider:
    """按 name 实例化 provider。"""
    list_providers()
    if name not in _REGISTRY:
        raise KeyError(f"未知 provider: {name}（可用: {list(_REGISTRY.keys())}）")
    cls = _REGISTRY[name]
    if name == "openai_compat":
        return cls(model=model, temperature=temperature, api_key=api_key, base_url=base_url, **kw)
    return cls(model=model, temperature=temperature, api_key=api_key, **kw)

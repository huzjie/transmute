# -*- coding: utf-8 -*-
"""工具注册表：`register_tool` 是装饰器工厂，返回 deco 再装饰真实函数。

⚠️ 坑：若 register_tool 同时既存 fn 又被当装饰器用，会踩「返回 fn 而非装饰器」的坑。
正确写法 = 装饰器工厂：`register_tool(name, desc)` 返回 deco，`@register_tool(name, desc)`
装饰真实函数。不要再包一层 `_xxx_tool` 转发。
"""
from __future__ import annotations

from typing import Callable, Dict, List, Optional

_REGISTRY: Dict[str, dict] = {}


def register_tool(name: str, description: str):
    """装饰器工厂：返回装饰器，把被装饰函数登记进注册表。"""
    def deco(fn: Callable) -> Callable:
        _REGISTRY[name] = {"name": name, "description": description, "fn": fn}
        return fn
    return deco


def list_tools() -> List[dict]:
    from . import read_file, write_file, run_test, git  # noqa: F401
    return sorted(_REGISTRY.values(), key=lambda t: t["name"])


def get_tool(name: str) -> Optional[dict]:
    list_tools()
    return _REGISTRY.get(name)


class ToolRegistry:
    """工具注册表外观：按白名单过滤出可调用工具。"""

    def __init__(self, allowed: Optional[List[str]] = None):
        self.allowed = set(allowed) if allowed else None

    def available(self) -> List[dict]:
        tools = list_tools()
        if self.allowed is None:
            return tools
        return [t for t in tools if t["name"] in self.allowed]

    def call(self, name: str, sandbox, *args, **kw):
        tool = get_tool(name)
        if tool is None:
            return {"ok": False, "error": f"未知工具: {name}"}
        if self.allowed is not None and name not in self.allowed:
            return {"ok": False, "error": f"工具 {name} 不在白名单内"}
        return tool["fn"](sandbox, *args, **kw)

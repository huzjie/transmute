# -*- coding: utf-8 -*-
"""read_file 工具。"""
from .registry import register_tool


@register_tool("read_file", "读取作用域内的文件内容")
def read_file(sandbox, rel: str) -> dict:
    return sandbox.read_file(rel)

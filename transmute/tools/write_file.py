# -*- coding: utf-8 -*-
"""write_file 工具。"""
from .registry import register_tool


@register_tool("write_file", "写入作用域内允许写的文件")
def write_file(sandbox, rel: str, content: str) -> dict:
    return sandbox.write_file(rel, content)

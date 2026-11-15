# -*- coding: utf-8 -*-
"""run_test 工具。"""
from .registry import register_tool


@register_tool("run_test", "在目标库内执行测试/构建命令")
def run_test(sandbox, cmd: str, cwd: str = "") -> dict:
    return sandbox.run_command(cmd, cwd or None)

# -*- coding: utf-8 -*-
"""Sandbox：在受限权限下执行智能体动作，拦截越界读写与网络访问。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from .filescope import FileScope
from .toolscope import ToolScope


@dataclass
class Sandbox:
    """把 FileScope + ToolScope 绑定起来，作为受控工具执行的统一入口。"""

    file_scope: FileScope
    tool_scope: ToolScope
    allow_network: bool = False
    read_only_outside_target: bool = True

    def _deny(self, msg: str) -> dict:
        return {"ok": False, "error": msg}

    def read_file(self, rel: str) -> dict:
        if not self.tool_scope.allow_tool("read_file"):
            return self._deny("read_file 不在工具白名单内")
        path = self.file_scope.resolve_read(rel)
        if path is None:
            return self._deny(f"越界或不可读: {rel}")
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return {"ok": True, "content": f.read()}
        except Exception as e:  # noqa: BLE001
            return self._deny(str(e))

    def write_file(self, rel: str, content: str) -> dict:
        if not self.tool_scope.allow_tool("write_file"):
            return self._deny("write_file 不在工具白名单内")
        path = self.file_scope.resolve_write(rel)
        if path is None:
            return self._deny(f"越界或不可写: {rel}")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"ok": True}
        except Exception as e:  # noqa: BLE001
            return self._deny(str(e))

    def run_command(self, cmd: str, cwd: Optional[str] = None) -> dict:
        """执行命令（默认禁止网络；命令由门禁白名单约束）。"""
        if not self.tool_scope.allow_tool("run_test"):
            return self._deny("run_test 不在工具白名单内")
        import subprocess
        try:
            proc = subprocess.run(
                cmd, shell=True, cwd=cwd or self.file_scope.root,
                capture_output=True, text=True, timeout=300,
            )
            return {"ok": True, "code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
        except Exception as e:  # noqa: BLE001
            return self._deny(str(e))

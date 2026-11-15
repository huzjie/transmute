# -*- coding: utf-8 -*-
"""Gate 抽象：一个门禁 = 跑命令 + 判断通过/失败 + 记录输出。"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass, field


@dataclass
class GateResult:
    passed: bool
    name: str
    command: str
    code: int = 0
    stdout: str = ""
    stderr: str = ""
    duration_ms: int = 0

    def brief(self) -> str:
        mark = "✅" if self.passed else "❌"
        return f"{mark} {self.name} (exit {self.code})"


class Gate:
    name = "gate"

    def __init__(self, command: str, timeout: int = 300, cwd: str = "."):
        self.command = command
        self.timeout = timeout
        self.cwd = cwd

    def run(self) -> GateResult:
        import time
        t0 = time.time()
        try:
            proc = subprocess.run(
                self.command, shell=True, cwd=self.cwd,
                capture_output=True, text=True, timeout=self.timeout,
            )
            code = proc.returncode
            out, err = proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as e:
            code = -1
            out = e.stdout or ""
            err = f"超时（>{self.timeout}s）"
        except Exception as e:  # noqa: BLE001
            code = -1
            out, err = "", str(e)
        dur = int((time.time() - t0) * 1000)
        return GateResult(
            passed=(code == 0), name=self.name, command=self.command,
            code=code, stdout=out, stderr=err, duration_ms=dur,
        )

# -*- coding: utf-8 -*-
"""Subtask 数据模型：迁移的最小可验证单元。"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Status(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    GENERATED = "generated"     # 候选已生成
    PASSED = "passed"           # 通过门禁
    REVIEWED = "reviewed"       # 复核通过
    MERGED = "merged"           # 已合并进主线
    REJECTED = "rejected"       # 门禁或复核不通过
    FAILED = "failed"           # 最终失败


@dataclass
class Subtask:
    """一个子任务：目标文件 + 最小读取作用域 + 工具作用域 + 验收测试。"""

    id: str
    title: str
    target: str                                   # 目标迁移单元（源 -> 目标）
    source_file: str
    dest_file: str
    read_scope: list = field(default_factory=list)   # 允许读取的上下文文件
    tool_scope: list = field(default_factory=list)   # 允许调用的工具
    acceptance: list = field(default_factory=list)   # 验收测试命令
    depends_on: list = field(default_factory=list)   # 依赖的子任务 id
    status: Status = Status.PENDING
    branch: str = ""
    candidate: str = ""                             # 候选代码
    report: str = ""                                # 失败/复核报告
    retries: int = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "target": self.target,
            "source_file": self.source_file,
            "dest_file": self.dest_file,
            "read_scope": self.read_scope,
            "tool_scope": self.tool_scope,
            "acceptance": self.acceptance,
            "depends_on": self.depends_on,
            "status": self.status.value,
            "branch": self.branch,
            "report": self.report,
            "retries": self.retries,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Subtask":
        s = cls(
            id=d["id"],
            title=d.get("title", d["id"]),
            target=d.get("target", ""),
            source_file=d.get("source_file", ""),
            dest_file=d.get("dest_file", ""),
            read_scope=d.get("read_scope", []),
            tool_scope=d.get("tool_scope", []),
            acceptance=d.get("acceptance", []),
            depends_on=d.get("depends_on", []),
        )
        s.status = Status(d.get("status", "pending"))
        s.branch = d.get("branch", "")
        s.candidate = d.get("candidate", "")
        s.report = d.get("report", "")
        s.retries = d.get("retries", 0)
        return s

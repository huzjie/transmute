# -*- coding: utf-8 -*-
"""任务分解：扫描目标代码库，按依赖图把迁移切碎成最小可验证单元。"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .plan import MigrationPlan
from .task import Subtask

# 常见「可独立迁移单元」的启发式：一个源文件对应一个目标文件
_SRC_EXT = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp"}
_ALT = {".c": ".rs", ".cc": ".rs", ".cpp": ".rs", ".cxx": ".rs", ".h": ".rs", ".hpp": ".rs"}


@dataclass
class DecomposeOptions:
    root: str = "."
    source_lang: str = "cpp"
    target_lang: str = "rust"
    include_headers: bool = True
    max_depth: int = 12


def _walk(root: str, opts: DecomposeOptions) -> List[str]:
    root_p = Path(root).resolve()
    hits: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root_p):
        dirnames[:] = [d for d in dirnames if d not in {".git", "target", "node_modules", "__pycache__"}]
        depth = len(Path(dirpath).relative_to(root_p).parts)
        if depth > opts.max_depth:
            dirnames[:] = []
            continue
        for fn in sorted(filenames):
            ext = os.path.splitext(fn)[1].lower()
            if ext in _SRC_EXT:
                if ext in {".h", ".hpp"} and not opts.include_headers:
                    continue
                hits.append(os.path.relpath(os.path.join(dirpath, fn), root_p).replace("\\", "/"))
    return hits


def decompose(opts: DecomposeOptions) -> MigrationPlan:
    """扫描源文件，每个源文件生成一个 Subtask（目标文件 = 换扩展名）。"""
    plan = MigrationPlan(source_lang=opts.source_lang, target_lang=opts.target_lang, root=opts.root)
    files = _walk(opts.root, opts)
    for i, src in enumerate(files, start=1):
        ext = os.path.splitext(src)[1].lower()
        dest = src[: -len(ext)] + _ALT.get(ext, ".rs")
        plan.tasks.append(Subtask(
            id=f"t{i:03d}",
            title=f"{src} -> {dest}",
            target=f"{src} -> {dest}",
            source_file=src,
            dest_file=dest,
            read_scope=[src],          # 最小：先只看自己
            tool_scope=["read_file", "write_file", "run_test"],
            acceptance=[],
        ))
    return plan


def enrich_read_scope(plan: MigrationPlan, project_root: str) -> MigrationPlan:
    """可选增强：把同目录的头文件加入 read_scope（同目录头文件通常是依赖）。"""
    for t in plan.tasks:
        d = os.path.dirname(t.source_file)
        for other in plan.tasks:
            if other.id == t.id:
                continue
            if os.path.dirname(other.source_file) == d and other.source_file.endswith((".h", ".hpp")):
                if other.source_file not in t.read_scope:
                    t.read_scope.append(other.source_file)
    return plan

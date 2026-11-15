# -*- coding: utf-8 -*-
"""依赖解析：基于 #include / use 声明做轻量依赖推断，回填 depends_on。"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, List

from ..task import Subtask

_INCLUDE_RE = re.compile(r'#\\s*include\\s*[<"]([^>"]+)[>"]')


def resolve_dependencies(tasks: List[Subtask], root: str) -> List[Subtask]:
    """扫描每个源文件的 include，把同库内被依赖的源文件写入 depends_on。

    这是「最小权限作用域」的反面补充：明确 A 依赖 B，切分时就能保证
    B 先于 A 迁移，避免 A 迁完引用一个还没迁的符号。
    """
    root_p = Path(root)
    src_by_name: Dict[str, str] = {}
    for t in tasks:
        src_by_name[os.path.basename(t.source_file)] = t.id
        src_by_name[os.path.basename(t.source_file).split(".")[0]] = t.id

    for t in tasks:
        path = root_p / t.source_file
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        deps = []
        for m in _INCLUDE_RE.finditer(text):
            header = os.path.basename(m.group(1))
            dep_id = src_by_name.get(header) or src_by_name.get(header.split(".")[0])
            if dep_id and dep_id != t.id and dep_id not in deps:
                deps.append(dep_id)
        t.depends_on = deps
    return tasks

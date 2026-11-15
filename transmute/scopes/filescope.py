# -*- coding: utf-8 -*-
"""FileScope：约束智能体只能读写哪些文件（最小权限的核心）。"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class FileScope:
    """read_scope = 可读文件；write_scope = 可写文件（通常只有目标文件）。"""

    root: str = "."
    read_scope: List[str] = field(default_factory=list)
    write_scope: List[str] = field(default_factory=list)

    def _norm(self, p: str) -> str:
        return os.path.normpath(p).replace("\\", "/")

    def can_read(self, rel: str) -> bool:
        rel = self._norm(rel)
        return rel in {self._norm(r) for r in self.read_scope}

    def can_write(self, rel: str) -> bool:
        rel = self._norm(rel)
        return rel in {self._norm(w) for w in self.write_scope}

    def resolve_read(self, rel: str) -> Optional[str]:
        """把相对路径解析为绝对路径（必须在 root 内且可读）。"""
        root = Path(self.root).resolve()
        target = (root / rel).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            return None
        if not self.can_read(rel):
            return None
        return str(target)

    def resolve_write(self, rel: str) -> Optional[str]:
        root = Path(self.root).resolve()
        target = (root / rel).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            return None
        if not self.can_write(rel):
            return None
        return str(target)


def resolve_path(root: str, rel: str) -> Optional[str]:
    """把相对路径安全解析到 root 内（越界返回 None）。"""
    root_p = Path(root).resolve()
    target = (root_p / rel).resolve()
    try:
        target.relative_to(root_p)
    except ValueError:
        return None
    return str(target)

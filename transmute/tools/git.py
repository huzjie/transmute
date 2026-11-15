# -*- coding: utf-8 -*-
"""git 工具（受限：只能分支/查看，不能 push）。"""
from .registry import register_tool

from ..gitops.repo import GitRepo


@register_tool("git_branch", "创建/切换分支（受控）")
def git_branch(sandbox, action: str, name: str = "") -> dict:
    try:
        repo = GitRepo(sandbox.file_scope.root)
        if action == "current":
            return {"ok": True, "branch": repo.current_branch()}
        if action == "create" and name:
            repo.checkout(name, create=True)
            return {"ok": True, "branch": name}
        return {"ok": False, "error": f"未知 action: {action}"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)}

# -*- coding: utf-8 -*-
"""分支 / 合并 / 回滚：一个子任务一条分支，失败即回滚。"""
from __future__ import annotations

from .repo import GitRepo, GitError


def create_branch(repo: GitRepo, name: str, base: str = "main") -> str:
    """从 base 建一条分支（子任务隔离）。"""
    repo.checkout(base)
    repo.checkout(name, create=True)
    return name


def merge_branch(repo: GitRepo, branch: str, target: str = "main", squash: bool = True) -> bool:
    """把 branch 合并进 target（squash）。"""
    repo.checkout(target)
    try:
        repo._run("merge", "--squash", branch)
        repo._run("commit", "-m", f"chore: squash merge {branch}")
        return True
    except GitError:
        return False


def rollback_branch(repo: GitRepo, branch: str, target: str = "main") -> None:
    """回滚：切回 target，删掉失败分支。"""
    repo.checkout(target)
    repo.delete_branch(branch)

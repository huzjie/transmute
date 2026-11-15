# -*- coding: utf-8 -*-
"""GitRepo：薄封装 git 命令（subprocess），失败抛出带输出的异常。"""
from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(RuntimeError):
    pass


class GitRepo:
    def __init__(self, root: str):
        self.root = str(Path(root).resolve())

    def _run(self, *args, check=True):
        proc = subprocess.run(
            ["git", "-C", self.root, *args],
            capture_output=True, text=True,
        )
        if check and proc.returncode != 0:
            raise GitError(f"git {' '.join(args)} 失败: {proc.stderr.strip()}")
        return proc

    def current_branch(self) -> str:
        return self._run("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()

    def is_dirty(self) -> bool:
        return bool(self._run("status", "--porcelain").stdout.strip())

    def checkout(self, branch: str, create: bool = False):
        if create:
            return self._run("checkout", "-b", branch)
        return self._run("checkout", branch)

    def commit_all(self, message: str):
        self._run("add", "-A")
        return self._run("commit", "-m", message)

    def reset_hard(self, ref: str = "HEAD"):
        return self._run("reset", "--hard", ref)

    def delete_branch(self, branch: str):
        return self._run("branch", "-D", branch, check=False)

    def merge_into(self, branch: str, squash: bool = True):
        """把当前分支 squash 合并到 branch。"""
        self._run("checkout", branch)
        args = ["merge", "--squash"]
        return self._run(*args, self._run("branch", "--show-current").stdout.strip())

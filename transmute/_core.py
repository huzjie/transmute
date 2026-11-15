# -*- coding: utf-8 -*-
"""确定性工具：字符串 seed → md5 派生 RNG，逐位可复现。"""
from __future__ import annotations

import hashlib
import random


def seed_from(label: str) -> int:
    """从任意字符串派生一个确定性 32-bit 种子（md5 前 8 字节）。

    同一 label 永远得到同一种子，保证两次运行结果逐位一致，
    便于回归测试与「回放」失败的迁移子任务。
    """
    digest = hashlib.md5(label.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") & 0xFFFFFFFF


class RNG:
    """包装 `random.Random`，统一 seed 语义，避免全局 random 污染。"""

    def __init__(self, seed: int | str | None = None):
        if seed is None:
            self._seed = 0
        elif isinstance(seed, str):
            self._seed = seed_from(seed)
        else:
            self._seed = seed & 0xFFFFFFFF
        self._rng = random.Random(self._seed)

    @property
    def seed(self) -> int:
        return self._seed

    def choice(self, seq):
        return self._rng.choice(seq)

    def shuffle(self, seq):
        self._rng.shuffle(seq)

    def randint(self, a, b):
        return self._rng.randint(a, b)

    def random(self):
        return self._rng.random()


def md5_short(data: bytes) -> str:
    """返回数据的 12 位 md5 摘要（用于报告/去重）。"""
    return hashlib.md5(data).hexdigest()[:12]

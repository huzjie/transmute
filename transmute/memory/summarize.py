# -*- coding: utf-8 -*-
"""上下文压缩：把「已合并符号表 + 说明」压缩成一段可塞进 Prompt 的摘要。"""
from __future__ import annotations

from typing import List

_MAX_SYMBOLS = 200


def summarize(merged_symbols: List[str], notes: List[str], max_symbols: int = _MAX_SYMBOLS) -> str:
    """把累积的全局上下文压成 Prompt 友好的紧凑文本，避免上下文无限膨胀。"""
    syms = sorted(merged_symbols)
    if len(syms) > max_symbols:
        shown = ", ".join(syms[:max_symbols])
        shown += f" ...（还有 {len(syms) - max_symbols} 个已迁移符号，见 plan）"
    elif syms:
        shown = ", ".join(syms)
    else:
        shown = "（尚无）"

    lines = [f"已迁移符号：{shown}"]
    if notes:
        lines.append("全局说明：" + "；".join(notes[-10:]))
    return "\n".join(lines)

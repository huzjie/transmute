# 静态检查门禁

## 实现

`gates/lint_gate.py`：跑 `clippy -D warnings` / `ruff`，把警告当错误。

## 复用要点

把 lint 的警告级别提到「报错」，逼候选代码一开始就干净，避免坏风格沉淀。

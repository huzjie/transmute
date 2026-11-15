# 复核智能体

## 实现

`agents/reviewer.py`：系统提示词强调「不写代码，只挑错」，带 `REVIEW_CHECKLIST` 逐条核对。

## 复用要点

复核者的提示词要点：**只许挑错、不许重写**，输出必须结构化（`<accept>` / `<reject>` + 位置 + 建议）。

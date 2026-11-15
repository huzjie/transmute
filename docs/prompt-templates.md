# 提示词模板

## 位置

`prompts/` 下的模板可直接复用：

- `generator.system.md` — 生成者
- `reviewer.system.md` — 复核者
- `planner.system.md` — 规划者
- `decompose.md` — 切分思路
- `workflow.md` — 端到端五步工作流

## 复用要点

模板里最值钱的是**职责分离**：generator 求「做出来」，reviewer 求「挑出毛病」。
两个角色用不同提示词、不同目标，比一个模型自问自答有效得多。

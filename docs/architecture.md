# 整体架构

## 一句话

把「大规模代码迁移」拆成「切分 → 生成 → 门禁 → 复核 → 合并/回滚」五步，每一步都有工程纪律兜底。

## 数据流

```
目标代码库
  → 依赖图切分（decompose）：一个源文件 = 一个子任务，标注依赖
  → 拓扑调度（scheduler）：批内并行、批间顺序
  → 生成（generator）：只读作用域内文件，产出候选
  → 门禁（gates）：compile → test → lint，任一失败即丢弃
  → 复核（reviewer）：挑错，职责与生成者分离
  → 合并/回滚（gitops）：通过才 squash 合并，失败自动回滚
```

## 分层

| 层 | 模块 | 职责 |
|---|---|---|
| 切分 | `core/` | task / plan / decompose + 依赖图 |
| 作用域 | `scopes/` | 文件/工具最小权限 + 沙箱 |
| 门禁 | `gates/` | compile / test / lint 三道路障 |
| 智能体 | `agents/` | planner / generator / reviewer |
| LLM | `llm/` | provider 抽象（openai_compat / anthropic / mock） |
| 编排 | `engine/` | orchestrator / scheduler / state |
| Git | `gitops/` | branch / merge / rollback |
| 服务 | `serve/` + `cli/` | FastAPI + 命令行 |

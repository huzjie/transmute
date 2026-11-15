# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-11-15

### Added
- 迁移计划核心：task / plan / decompose（依赖图切分）(`core/`)
- 智能体：planner / generator / reviewer 职责分离 (`agents/`)
- 最小权限作用域：filescope / toolscope / sandbox (`scopes/`)
- 测试门禁：compile / test / lint / pipeline (`gates/`)
- LLM 适配：openai_compat / anthropic / mock (`llm/`)
- 上下文管理：context / store / summarize (`memory/`)
- Git 操作：branch / merge / rollback (`gitops/`)
- 编排引擎：orchestrator / scheduler / state (`engine/`)
- CLI（plan / doctor / run / status / report）+ FastAPI + Python/TS SDK + Web 控制台
- 提示词模板、40+ 篇技术文档、示例、Docker/K8s/Helm/CI

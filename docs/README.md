# 文档索引

按「原理 → 实现 → 复用思路」组织，建议按顺序读。

## 入门
- [getting-started.md](getting-started.md) — 快速开始
- [architecture.md](architecture.md) — 整体架构
- [configuration.md](configuration.md) — 配置说明
- [why-transmute.md](why-transmute.md) — 为什么需要 transmute

## 方法论（干货核心）
- [zircon-rewrite.md](zircon-rewrite.md) — Zircon 微内核 C++→Rust 改写方法论解读
- [task-decomposition.md](task-decomposition.md) — 任务切分
- [least-privilege.md](least-privilege.md) — 最小权限作用域
- [test-gating.md](test-gating.md) — 测试门禁
- [dual-agent-review.md](dual-agent-review.md) — 双智能体复核
- [rollback-repro.md](rollback-repro.md) — 回滚与复现

## 实现拆解
- [decompose.md](decompose.md) — 依赖图切分
- [filescope.md](filescope.md) — 文件作用域
- [toolscope.md](toolscope.md) — 工具作用域
- [sandbox.md](sandbox.md) — 沙箱
- [compile-gate.md](compile-gate.md) — 编译门禁
- [test-gate.md](test-gate.md) — 测试门禁
- [lint-gate.md](lint-gate.md) — 静态检查门禁
- [generator-agent.md](generator-agent.md) — 生成智能体
- [reviewer-agent.md](reviewer-agent.md) — 复核智能体
- [prompt-templates.md](prompt-templates.md) — 提示词模板
- [orchestrator.md](orchestrator.md) — 编排引擎
- [scheduler.md](scheduler.md) — 拓扑调度

## LLM 与上下文
- [providers.md](providers.md) — LLM 适配
- [context-management.md](context-management.md) — 上下文管理
- [memory-store.md](memory-store.md) — 记忆持久化
- [determinism.md](determinism.md) — 确定性

## 语言迁移专题
- [cpp-to-rust.md](cpp-to-rust.md) — C++ → Rust 迁移
- [memory-safety.md](memory-safety.md) — 内存安全
- [semantic-equivalence.md](semantic-equivalence.md) — 语义等价
- [ownership.md](ownership.md) — 所有权与借用
- [unsafe-bridge.md](unsafe-bridge.md) — unsafe 桥接

## 工程与部署
- [serving.md](serving.md) — 服务
- [sdk.md](sdk.md) — SDK
- [web-console.md](web-console.md) — Web 控制台
- [deployment.md](deployment.md) — 部署
- [docker.md](docker.md) — Docker
- [k8s-helm.md](k8s-helm.md) — K8s/Helm
- [ci-cd.md](ci-cd.md) — CI/CD

## 参考
- [benchmark.md](benchmark.md) — 基准
- [faq.md](faq.md) — FAQ
- [troubleshooting.md](troubleshooting.md) — 排错
- [glossary.md](glossary.md) — 术语表
- [security.md](security.md) — 安全
- [limitations.md](limitations.md) — 局限与边界

## 配方（recipes）
- [cpp-to-rust.md](recipes/cpp-to-rust.md) — C++ 类 → Rust 结构体
- [pointer-to-ownership.md](recipes/pointer-to-ownership.md) — 裸指针 → 所有权
- [header-to-module.md](recipes/header-to-module.md) — 头文件 → 模块
- [review-checklist.md](recipes/review-checklist.md) — 复核找茬清单
- [test-first.md](recipes/test-first.md) — 测试先行

## 高级（advanced）
- [retry-strategy.md](advanced/retry-strategy.md) — 失败重试策略
- [parallel-safety.md](advanced/parallel-safety.md) — 并行安全
- [context-compression.md](advanced/context-compression.md) — 上下文压缩
- [deterministic-rng.md](advanced/deterministic-rng.md) — 确定性 RNG
- [multi-language.md](advanced/multi-language.md) — 迁移到其他语言

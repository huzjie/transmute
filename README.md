# transmute — 多智能体验证式代码迁移编排引擎

> 把「80 万行 C++ 安全改写成 Rust 并全部通过单元测试」这件事，拆成一套可复用的工程方法：
> **任务切分（最小权限）→ 候选生成（测试门禁）→ 双智能体复核 → 可回滚可复现**。
> 填好 LLM 配置，把项目路径喂进去，它就能在真实代码库上跑完端到端迁移。

**transmute** 不是又一个「让 AI 帮你改代码」的聊天工具，而是一套**有工程纪律的代码迁移编排引擎**。
它的方法论直接来自 Google Research 2026-11-13 公布的多智能体协作成果——把 Zircon 微内核剩余的
C++ 代码重写为约 80 万行安全 Rust 并通过全部内核单元测试。我们把这套「怎么做才敢在 OS 内核这种
高危代码上放手让 AI 改」的方法，落成可独立运行、可复用的完整工程。

---

## 为什么这很硬核：AI 改代码的「信任问题」

让一个模型改一段代码很简单，但让它在**几十万行、关乎正确性的代码库**里做大规模迁移，难点不在
「能不能写对一行」，而在「怎么证明改完没坏」。transmute 把这个问题拆成四道关卡：

| 关卡 | 解决什么问题 | 关键机制 |
|---|---|---|
| 任务切分 + 最小权限作用域 | 范围失控：AI 改到不该改的文件 | 每个智能体只拿到本步骤所需文件与工具 |
| 测试门禁（compile + test + lint） | 正确性无法自证：AI 说"好了"不等于真的好了 | 候选结果必须通过测试套件才进下一环 |
| 双智能体复核 | 幻觉风险：单一智能体自我感觉良好 | 生成者只管写、复核者只管挑错，职责分离 |
| 分支隔离 + 回滚 | 坏改动污染主干 | 一个子任务一条分支，不过门禁就回滚 |

这四关没有一个是「新技术」，但把它们**串成一条可验证、可回滚、可复现的流水线**，才是把「AI 改代码」
从玩具变成生产工具的分水岭。下面逐个拆「怎么实现 + 为什么这么做」，每一条都对应到仓库里能跑的模块。

---

## 技术拆解一：任务切分与最小权限作用域

大规模迁移最怕「一个大 Prompt 让模型从 0 改到 1」。正确做法是**先拆后改**：把整个迁移按依赖关系
切成细粒度子任务，每个子任务只绑定它真正需要的输入文件（文件作用域）和工具（工具作用域）。

```python
# 子任务 = 目标文件 + 允许读取的上下文文件 + 允许调用的工具 + 验收测试
subtask = Subtask(
    target="zircon/kernel/mutex.cc -> mutex.rs",
    read_scope=["zircon/kernel/mutex.h", "zircon/kernel/types.h"],   # 只让看这几个
    tool_scope=["read_file", "write_file", "run_test"],               # 只让用这几个
    acceptance=["zircon/kernel/tests/mutex_test"],                     # 用测试证明
)
```

对应实现见 [`transmute/core/decompose.py`](transmute/core/decompose.py)（按依赖图切分）与
[`transmute/scopes/`](transmute/scopes/)（文件/工具最小权限）。**可复用要点**：给 AI 的权限越窄，
它「越界改坏」的可能性越低——最小权限不是限制能力，是**把错误隔离在最小的可控单元里**。

## 技术拆解二：测试门禁 —— 让测试套件当「唯一真值」

AI 改完说"应该没问题"是不可信的。transmute 的核心纪律是：**候选代码必须先过三道路障**，任何一关
不过就直接丢弃、不进入复核。

```
compile gate ──► test gate ──► lint gate
  (能编译)      (单测全绿)     (静态检查)
      │ 失败 → 回滚，写进失败报告，换下一策略重试（最多 N 次）
```

对应实现见 [`transmute/gates/`](transmute/gates/)：`compile_gate.py` 跑 `cargo build`/编译器，
`test_gate.py` 跑目标测试，`lint_gate.py` 跑 `clippy`/`ruff`，`pipeline.py` 把三者串成可插拔管线。
**可复用要点**：测试套件是迁移的正确性「锚点」——没有可执行测试的代码，AI 迁移就是盲人摸象。
所以在迁移前**先补齐目标模块的测试**，比急着改代码重要得多。

## 技术拆解三：双智能体复核 —— 生成与挑错职责分离

单个智能体写代码时会「自我感觉良好」，因为它刚刚是自己生成的。transmute 用**两组智能体**解耦：

```python
generator = Agent(role="generator")   # 只负责：读作用域内文件 → 产出候选迁移
reviewer  = Agent(role="reviewer")    # 只负责：挑错（正确性/内存安全/遗漏/越界）
# 复核不是"再生成一遍"，而是带着「找茬清单」逐条核对候选
```

对应实现见 [`transmute/agents/`](transmute/agents/)：`generator.py` 产出候选、`reviewer.py` 用
`REVIEW_CHECKLIST` 挑错，复核不通过则带着批注打回生成者重写。**可复用要点**：让 AI「自己审自己」
几乎无效——两个角色必须**用不同的系统提示词、不同的目标函数**，一个求"做出来"、一个求"挑出毛病"，
这比让一个模型自问自答有用得多。

## 技术拆解四：分支隔离与确定性回滚

一个子任务一条 Git 分支，通过门禁 + 复核才 `squash` 合并进主线；失败即回滚，全程可复现。

```python
# 确定性 RNG：字符串 seed → md5 前 8 字节，逐位可复现（回归测试 / 回放一致）
rng = seed_from("mutex.cc -> mutex.rs")
```

对应实现见 [`transmute/gitops/`](transmute/gitops/)（分支/合并/回滚）与
[`transmute/_core.py`](transmute/_core.py)（`seed_from` / `RNG`）。**可复用要点**：可回滚不是「备份一份」，
而是**把每一次变更都变成可寻址、可撤销的提交**；可复现则靠确定性 RNG，否则同样输入两次跑出不同结果，
排错和回放都无从谈起。

---

## 一个可直接复用的「干货块」：最小可跑配置 + 提示词模板

克隆后复制配置、填上 LLM 端点即可在真实项目上跑（内核零依赖，`pip install -e .` 只装服务端可选依赖）：

```yaml
# config.yaml —— 一次真实迁移的最小配置
llm:
  provider: openai_compat          # 任意 OpenAI 风格端点（或 anthropic / mock）
  base_url: http://localhost:11434/v1
  model: qwen3.8
  api_key_env: TM_API_KEY          # 密钥走环境变量，不落盘

migration:
  root: ./zircon                   # 目标代码库
  source_lang: cpp
  target_lang: rust
  plan_file: ./migration.plan.json # 迁移计划（切分结果）

gates:
  compile: { command: "cargo build", timeout: 300 }
  test:    { command: "cargo test",  timeout: 600 }
  lint:    { command: "cargo clippy -- -D warnings", timeout: 300 }

agents:
  generator: { model: qwen3.8, max_retries: 3 }
  reviewer:  { model: qwen3.8, strictness: high }
```

```bash
# 生成迁移计划（按依赖图把任务切碎，落成 plan.json）
transmute plan --config config.yaml
# 自检 9 项（作用域 / 门禁 / 双智能体 / 回滚 / 确定性 ...）
transmute doctor
# 跑完整迁移（切分 → 生成 → 门禁 → 复核 → 合并/回滚）
transmute run --config config.yaml
```

### 内置提示词模板（`prompts/` 下可直接改）

`prompts/generator.system.md`（生成者，求「做出来」）：

```markdown
你是 C++→Rust 迁移工程师。你**只能**读取 `<read_scope>` 列出的文件、只能调用
`<tool_scope>` 列出的工具。你的唯一产出是目标文件的完整 Rust 重写，要求：
1. 语义等价：不新增/不删减任何行为，逐函数对齐原语义；
2. 内存安全：所有权、借用、生命周期写对，禁止 unsafe（除非有注释说明理由）；
3. 不做无关重构：不顺手改命名、不优化、不删注释。
完成后用 `run_test` 跑 `<acceptance>`，通过后再提交候选。
```

`prompts/reviewer.system.md`（复核者，求「挑出毛病」）：

```markdown
你是 C++→Rust 迁移的审校员。你**不写代码**，只负责从候选里挑错。逐条核对：
1. 语义等价：有没有漏函数、改控制流、改常量？
2. 内存安全：有没有 data race、use-after-free、错误的所有权转移？
3. 边界：整数溢出、索引越界、null 处理是否对齐原语义？
4. 越界：是否改动/引用了 read_scope 之外的文件？
任何一项不达标 → 输出 `<reject>` + 具体行号 + 修复建议；全部达标才输出 `<accept>`。
```

这两个模板可以直接拿去喂任意模型，是本次「双智能体职责分离」的完整可复用配方。

---

## 目录结构

```
transmute/
├── core/         迁移计划：task / plan / decompose（依赖图切分）
├── agents/       智能体：planner / generator / reviewer（职责分离）
├── scopes/       最小权限：filescope / toolscope / sandbox
├── gates/        测试门禁：compile / test / lint / pipeline
├── llm/          LLM 适配：openai_compat / anthropic / mock
├── memory/       上下文管理：context / store / summarize
├── gitops/       Git 操作：branch / merge / rollback
├── engine/       编排：orchestrator / scheduler / state
├── tools/        受控工具：read_file / write_file / run_test / git
├── cli/          命令行：plan / doctor / run / status / report
├── serve/        FastAPI：/v1/migrations / /health
├── sdk/          Python + TypeScript 客户端
├── web/          Web 控制台（单文件）
├── prompts/      提示词模板（可直接复用）
└── docs/         40+ 篇技术文档（原理 + 实现 + 复用思路）
```

## 快速开始

见 [`docs/getting-started.md`](docs/getting-started.md)。一句话：`pip install -e .` → 改 `config.yaml` → `transmute doctor` 自检 → `transmute run` 跑迁移。

## License

MIT © 智能交付知识工程组 编（教学/研究参考实现，方法源自公开报道的 Google Research 多智能体协作成果）

# 示例

`demo/` 是一个最小 C++ 项目，用 mock provider 即可跑通 transmute 全流程（无需真实 LLM）。

```bash
cd examples/demo
transmute plan --config config.yaml
transmute run --config config.yaml
transmute status --plan migration.plan.json
```

mock provider 会把 prompt 原样回显，适合验证「切分 → 生成 → 门禁 → 复核」的链路
是否连通，再替换成真实 LLM 端点做真实迁移。

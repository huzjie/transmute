# LLM 适配

`llm/` 抽象统一 `complete` / `chat` 接口，内置：

- openai_compat（任意 OpenAI 风格端点）
- anthropic（Messages API）
- mock（无 LLM 冒烟）

## 复用要点

注册表存**实例**而非类，惰性 import 触发注册。provider 用「装饰器工厂」注册，
别既存 fn 又当装饰器用（会踩「返回 fn 而非装饰器」的坑）。

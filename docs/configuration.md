# 配置说明

配置文件 `config.yaml`（参考 `config.example.yaml`）。

## llm

- `provider`：openai_compat / anthropic / mock。
- `base_url` / `model`：端点与模型名。
- `api_key_env`：密钥所在的环境变量名（不落盘）。

## migration

- `root`：目标代码库路径。
- `source_lang` / `target_lang`：源/目标语言。
- `plan_file`：切分结果落盘路径。
- `max_parallel`：并行子任务数（受依赖图约束）。

## gates

- `compile.command` / `test.command` / `lint.command`：三道门禁命令。
- `*.timeout`：每道门禁超时秒数。

## agents

- `generator.max_retries`：生成失败重试次数。
- `reviewer.strictness`：复核严格度（high 从严）。

## scopes

- `allow_network`：是否允许智能体联网（默认 false）。
- `read_only_outside_target`：目标之外只读（默认 true）。

## serve

- `host` / `port`：服务绑定（默认 127.0.0.1:8000，公网请加鉴权）。

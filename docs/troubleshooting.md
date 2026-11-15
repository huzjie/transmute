# 排错

| 症状 | 原因 | 解法 |
|---|---|---|
| 生成候选为空 | provider 配置错 | 检查 base_url / model / api_key_env |
| 门禁一直失败 | 命令写错或超时 | 检查 gates 命令与 timeout |
| 复核一直 reject | 候选语义不等价 | 看 report 定位，缩小 read_scope 后重试 |
| 越界读写被拦 | read/write_scope 没配 | 在切分结果里补对应文件 |
| doctor 失败 | 依赖缺 | `pip install -e ".[dev]"` |

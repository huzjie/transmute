# Contributing

感谢贡献。流程：fork → 开分支 → 提交 → 提 PR。

## 开发环境

```bash
pip install -e ".[dev]"
pytest -q
ruff check .
```

## 提交规范

- 遵循 Conventional Commits：`feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:`
- 新增子系统需附带单测与 `docs/` 对应文档
- 涉及门禁/作用域的改动需通过 `transmute doctor` 自检

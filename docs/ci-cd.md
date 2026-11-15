# CI/CD

`.github/workflows/`：

- `ci.yml`：doctor 自检 + pytest + ruff
- `codeql.yml`：安全扫描
- `release.yml`：打 tag 自动构建 wheel 发布 PyPI

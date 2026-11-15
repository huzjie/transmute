# 快速开始

## 安装

```bash
git clone https://github.com/huzjie/transmute.git
cd transmute
pip install -e .            # 零依赖内核
pip install -e ".[serve]"   # 起服务需要
```

## 自检

```bash
transmute doctor
```

输出 9 项自检，全绿即可跑。

## 生成迁移计划

```bash
cp config.example.yaml config.yaml
transmute plan --config config.yaml
# 产出 migration.plan.json（按依赖图切分好的子任务）
```

## 跑完整迁移

```bash
transmute run --config config.yaml
```

## 查看进度 / 失败报告

```bash
transmute status --plan migration.plan.json
transmute report --plan migration.plan.json
```

## 用 SDK 调用

```python
from transmute.sdk import TransmuteClient
c = TransmuteClient()
print(c.health())
print(c.create_migration("config.yaml"))
```

## 跑测试

```bash
pip install -e ".[dev]"
pytest -q
```

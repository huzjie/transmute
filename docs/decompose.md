# 依赖图切分

## 实现

`core/decompose.py`：扫描目标代码库，每个源文件生成一个 Subtask（目标文件 = 换扩展名）。

`core/dependency/graph.py`：按 `depends_on` 构建 DAG，拓扑分批——同一批内无相互依赖，
可并行执行。

`core/dependency/resolve.py`：扫描 `#include` 声明，把同库内被依赖的源文件回填进
`depends_on`，保证被依赖者先迁移。

## 复用要点

拓扑分批是「依赖驱动的并行」——凡是任务间有先后依赖的批量作业，都能用这一招安全并行。

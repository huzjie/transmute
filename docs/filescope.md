# 文件作用域

## 实现

`scopes/filescope.py` 的 `FileScope`：

- `read_scope`：允许读取的上下文文件；
- `write_scope`：允许写入的文件（通常只有目标文件）；
- `resolve_read` / `resolve_write`：把相对路径安全解析到 root 内，越界返回 None。

## 复用要点

路径解析一定要做「解析后再校验是否在 root 内」，用 `Path.resolve()` + `relative_to()`
防 `../` 逃逸。

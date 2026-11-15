# 工具作用域

## 实现

`scopes/toolscope.py` 的 `ToolScope`：白名单工具集合，`allow_tool` 判断。

## 复用要点

工具白名单要显式枚举，别用黑名单——黑名单永远漏。

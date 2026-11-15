# 配方：头文件 → Rust 模块

## 步骤

1. `.h` 声明 → `mod.rs` 或同名 `.rs`；
2. `.cc` 实现 → 同模块 `impl` 块；
3. `#include` → `use` / `mod`；
4. `#define` 常量 → `const`，宏 → 普通函数或 `const fn`。

## 提示

头文件与实现文件在 Rust 里通常是同一个文件，别机械一比一搬。

"""最小权限作用域：文件 / 工具 / 沙箱。"""
from .filescope import FileScope, resolve_path
from .toolscope import ToolScope, allow_tool
from .sandbox import Sandbox

__all__ = ["FileScope", "resolve_path", "ToolScope", "allow_tool", "Sandbox"]

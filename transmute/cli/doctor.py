# -*- coding: utf-8 -*-
"""doctor 自检：9 项，全绿即可跑。"""
from __future__ import annotations

from .._core import RNG, seed_from
from ..config import load_config
from ..core.decompose import DecomposeOptions, decompose
from ..core.dependency.graph import DependencyGraph
from ..gates.compile_gate import CompileGate
from ..llm.registry import list_providers
from ..scopes.filescope import FileScope
from ..scopes.sandbox import Sandbox
from ..scopes.toolscope import ToolScope
from ..tools.registry import list_tools


def run_doctor() -> bool:
    checks = []
    try:
        # 1. 确定性 RNG
        a, b = seed_from("mutex.cc"), seed_from("mutex.cc")
        checks.append(("确定性 RNG", a == b))
        # 2. 配置加载
        cfg = load_config(None)
        checks.append(("配置加载", cfg.llm_provider == "mock"))
        # 3. 任务切分（空目录也可切分）
        plan = decompose(DecomposeOptions(root=".", source_lang="cpp", target_lang="rust"))
        checks.append(("任务切分", isinstance(plan.tasks, list)))
        # 4. 依赖图
        from ..core.task import Subtask
        t1 = Subtask(id="a", title="a", target="a", source_file="a", dest_file="a.rs")
        t2 = Subtask(id="b", title="b", target="b", source_file="b", dest_file="b.rs", depends_on=["a"])
        g = DependencyGraph([t1, t2])
        checks.append(("依赖图拓扑", g.topological_order() == ["a", "b"]))
        # 5. provider 注册
        providers = list_providers()
        checks.append(("LLM provider", "mock" in providers))
        # 6. 工具注册表
        tools = [t["name"] for t in list_tools()]
        checks.append(("工具注册表", all(x in tools for x in ["read_file", "write_file", "run_test"])))
        # 7. 文件作用域越界拦截
        fs = FileScope(root=".", read_scope=["a"], write_scope=["a.rs"])
        checks.append(("文件作用域", fs.resolve_read("../etc/passwd") is None))
        # 8. 沙箱工具白名单
        sb = Sandbox(file_scope=fs, tool_scope=ToolScope(["read_file"]))
        checks.append(("沙箱白名单", sb.write_file("a.rs", "x")["ok"] is False))
        # 9. 门禁（mock 命令，应能跑）
        from ..gates.pipeline import GatePipeline
        from ..gates.test_gate import TestGate
        res = GatePipeline([TestGate("python -c \"print(1)\"" if __import__("sys").platform != "win32" else "python -c \"print(1)\"", 30, ".")]).run()
        checks.append(("门禁管线", isinstance(res, list)))
    except Exception as e:  # noqa: BLE001
        checks.append(("异常", False))
        print(f"  异常: {e}")

    all_ok = True
    for name, ok in checks:
        mark = "✅" if ok else "❌"
        print(f"  {mark} {name}")
        all_ok = all_ok and ok
    print("doctor 结果：" + ("全绿，可运行" if all_ok else "存在失败项"))
    return all_ok

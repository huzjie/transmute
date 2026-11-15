# -*- coding: utf-8 -*-
from transmute.scopes.filescope import FileScope
from transmute.scopes.sandbox import Sandbox
from transmute.scopes.toolscope import ToolScope


def test_filescope_outside_blocked():
    fs = FileScope(root=".", read_scope=["a.cc"], write_scope=["a.rs"])
    assert fs.resolve_read("../etc/passwd") is None
    assert fs.resolve_read("a.cc") is not None


def test_sandbox_tool_whitelist():
    fs = FileScope(root=".", read_scope=["a"], write_scope=["a.rs"])
    sb = Sandbox(file_scope=fs, tool_scope=ToolScope(["read_file"]))
    assert sb.write_file("a.rs", "x")["ok"] is False
    assert sb.read_file("a.rs")["ok"] is False  # 不在 read_scope


def test_sandbox_read_scope():
    import tempfile, os
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "a.cc")
        with open(p, "w") as f:
            f.write("int x;")
        fs = FileScope(root=d, read_scope=["a.cc"], write_scope=["a.rs"])
        sb = Sandbox(file_scope=fs, tool_scope=ToolScope(["read_file", "write_file"]))
        assert sb.read_file("a.cc")["ok"] is True
        assert sb.write_file("a.rs", "fn main(){}")["ok"] is True

# -*- coding: utf-8 -*-
import os
import tempfile

from transmute.core.decompose import DecomposeOptions, decompose


def test_decompose_finds_cpp(tmp_path):
    (tmp_path / "a.cc").write_text("int x;")
    (tmp_path / "b.h").write_text("// h")
    (tmp_path / "readme.md").write_text("no")
    opts = DecomposeOptions(root=str(tmp_path), source_lang="cpp", target_lang="rust")
    plan = decompose(opts)
    names = {t.source_file for t in plan.tasks}
    assert "a.cc" in names
    assert "b.h" in names
    assert "readme.md" not in names
    # 目标文件扩展名替换
    for t in plan.tasks:
        assert t.dest_file.endswith(".rs")


def test_decompose_dest_extension():
    plan = decompose(DecomposeOptions(root=".", source_lang="cpp", target_lang="rust"))
    for t in plan.tasks:
        assert not t.dest_file.endswith((".cc", ".cpp", ".h", ".hpp"))

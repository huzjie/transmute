# -*- coding: utf-8 -*-
from transmute.llm.registry import get_provider, list_providers
from transmute.tools.registry import list_tools, get_tool


def test_providers():
    providers = list_providers()
    assert "mock" in providers
    assert "openai_compat" in providers


def test_mock_provider():
    p = get_provider("mock")
    r = p.complete("hello")
    assert "hello" in r.text


def test_tools_registered():
    names = [t["name"] for t in list_tools()]
    for want in ["read_file", "write_file", "run_test", "git_branch"]:
        assert want in names

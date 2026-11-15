# -*- coding: utf-8 -*-
from transmute.gates.compile_gate import CompileGate
from transmute.gates.lint_gate import LintGate
from transmute.gates.pipeline import GatePipeline
from transmute.gates.test_gate import TestGate


def test_gate_pass():
    import sys
    ok = "python -c \"print(1)\"" if sys.platform != "win32" else "python -c \"print(1)\""
    r = TestGate(ok, 30, ".").run()
    assert r.passed


def test_gate_fail():
    r = TestGate("python -c \"import sys; sys.exit(3)\"", 30, ".").run()
    assert not r.passed


def test_pipeline_short_circuit():
    fail = LintGate("python -c \"import sys; sys.exit(1)\"", 30, ".")
    ok = TestGate("python -c \"print(1)\"", 30, ".")
    results = GatePipeline([fail, ok]).run()
    assert len(results) == 1  # 短路

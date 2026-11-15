# -*- coding: utf-8 -*-
from transmute.core.dependency.graph import DependencyGraph, topological_batches
from transmute.core.task import Subtask


def _mk(tid, deps=()):
    return Subtask(id=tid, title=tid, target=tid, source_file=tid, dest_file=tid + ".rs",
                   depends_on=list(deps))


def test_topo_order():
    t1 = _mk("a")
    t2 = _mk("b", ["a"])
    t3 = _mk("c", ["a"])
    g = DependencyGraph([t1, t2, t3])
    order = g.topological_order()
    assert order.index("a") < order.index("b")
    assert order.index("a") < order.index("c")


def test_batches_parallel():
    tasks = [_mk("a"), _mk("b", ["a"]), _mk("c", ["a"]), _mk("d", ["b", "c"])]
    batches = topological_batches(tasks, limit=10)
    assert batches[0] == ["a"]
    assert set(batches[1]) == {"b", "c"}
    assert batches[2] == ["d"]

# -*- coding: utf-8 -*-
import json

from transmute.core.plan import MigrationPlan
from transmute.core.task import Subtask, Status


def test_plan_roundtrip(tmp_path):
    t = Subtask(id="t1", title="a", target="a.cc -> a.rs",
                source_file="a.cc", dest_file="a.rs")
    t.status = Status.PASSED
    plan = MigrationPlan(root=".", tasks=[t])
    p = tmp_path / "plan.json"
    plan.save(str(p))
    loaded = MigrationPlan.load(str(p))
    assert loaded.by_id("t1").dest_file == "a.rs"
    assert loaded.by_id("t1").status == Status.PASSED

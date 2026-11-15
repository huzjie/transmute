# -*- coding: utf-8 -*-
'''最小 C++ 迁移示例：直接调用 API 跑一次迁移。'''
from transmute.config import load_config
from transmute.engine.orchestrator import Orchestrator

if __name__ == "__main__":
    cfg = load_config("examples/demo/config.yaml")
    result = Orchestrator(config=cfg).run()
    print(result["summary"])

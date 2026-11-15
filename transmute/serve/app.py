# -*- coding: utf-8 -*-
"""FastAPI 应用：提交迁移 / 查状态 / 健康检查。"""
from __future__ import annotations


def create_app():
    try:
        from fastapi import FastAPI
        from fastapi.responses import JSONResponse
    except Exception:  # pragma: no cover - serve 为可选依赖
        raise ImportError("需要安装 serve 依赖：pip install -e \"[serve]\"")

    from .._core import md5_short
    from ..config import load_config
    from ..engine.orchestrator import Orchestrator

    app = FastAPI(title="transmute", version="0.1.0")

    _JOBS = {}

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "transmute"}

    @app.post("/v1/migrations")
    def create_migration(payload: dict):
        """提交一次迁移。body: {config: "config.yaml"}"""
        cfg = load_config(payload.get("config"))
        orch = Orchestrator(config=cfg)
        plan = orch.build_plan()
        job_id = md5_short((cfg.migration_root + str(len(_JOBS))).encode("utf-8"))
        _JOBS[job_id] = {"plan": plan, "status": "planned", "summary": plan.summary()}
        return JSONResponse({"id": job_id, "status": "planned", "summary": plan.summary()})

    @app.get("/v1/migrations/{job_id}")
    def get_migration(job_id: str):
        job = _JOBS.get(job_id)
        if job is None:
            return JSONResponse({"error": "not found"}, status_code=404)
        return {"id": job_id, "status": job["status"], "summary": job["summary"]}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

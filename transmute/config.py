# -*- coding: utf-8 -*-
"""配置加载：config.yaml -> Config 数据类，缺省值兜底。"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Config:
    llm_provider: str = "mock"
    llm_base_url: str = ""
    llm_model: str = "mock"
    llm_api_key_env: str = "TM_API_KEY"
    llm_temperature: float = 0.2
    migration_root: str = "."
    source_lang: str = "cpp"
    target_lang: str = "rust"
    plan_file: str = "migration.plan.json"
    max_parallel: int = 4
    compile_cmd: str = "cargo build"
    compile_timeout: int = 300
    test_cmd: str = "cargo test"
    test_timeout: int = 600
    lint_cmd: str = "cargo clippy -- -D warnings"
    lint_timeout: int = 300
    generator_model: str = "mock"
    generator_max_retries: int = 3
    reviewer_model: str = "mock"
    reviewer_strictness: str = "high"
    allow_network: bool = False
    read_only_outside_target: bool = True
    serve_host: str = "127.0.0.1"
    serve_port: int = 8000
    extra: dict = field(default_factory=dict)

    def api_key(self) -> str:
        return os.environ.get(self.llm_api_key_env, "")


def _try_import_yaml():
    try:
        import yaml  # type: ignore
        return yaml
    except Exception:
        return None


def load_config(path: str | None = None) -> Config:
    """加载 config.yaml（可选）。没有文件则返回默认 Config。"""
    cfg = Config()
    if not path:
        return cfg
    p = Path(path)
    if not p.exists():
        return cfg
    yaml = _try_import_yaml()
    if yaml is None:
        return cfg
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return _apply(cfg, data)


def _apply(cfg: Config, data: dict) -> Config:
    llm = data.get("llm", {})
    if isinstance(llm, dict):
        cfg.llm_provider = llm.get("provider", cfg.llm_provider)
        cfg.llm_base_url = llm.get("base_url", cfg.llm_base_url)
        cfg.llm_model = llm.get("model", cfg.llm_model)
        cfg.llm_api_key_env = llm.get("api_key_env", cfg.llm_api_key_env)
        cfg.llm_temperature = llm.get("temperature", cfg.llm_temperature)
    mig = data.get("migration", {})
    if isinstance(mig, dict):
        cfg.migration_root = mig.get("root", cfg.migration_root)
        cfg.source_lang = mig.get("source_lang", cfg.source_lang)
        cfg.target_lang = mig.get("target_lang", cfg.target_lang)
        cfg.plan_file = mig.get("plan_file", cfg.plan_file)
        cfg.max_parallel = mig.get("max_parallel", cfg.max_parallel)
    gates = data.get("gates", {})
    if isinstance(gates, dict):
        c = gates.get("compile", {})
        t = gates.get("test", {})
        l = gates.get("lint", {})
        if isinstance(c, dict):
            cfg.compile_cmd = c.get("command", cfg.compile_cmd)
            cfg.compile_timeout = c.get("timeout", cfg.compile_timeout)
        if isinstance(t, dict):
            cfg.test_cmd = t.get("command", cfg.test_cmd)
            cfg.test_timeout = t.get("timeout", cfg.test_timeout)
        if isinstance(l, dict):
            cfg.lint_cmd = l.get("command", cfg.lint_cmd)
            cfg.lint_timeout = l.get("timeout", cfg.lint_timeout)
    agents = data.get("agents", {})
    if isinstance(agents, dict):
        g = agents.get("generator", {})
        r = agents.get("reviewer", {})
        if isinstance(g, dict):
            cfg.generator_model = g.get("model", cfg.generator_model)
            cfg.generator_max_retries = g.get("max_retries", cfg.generator_max_retries)
        if isinstance(r, dict):
            cfg.reviewer_model = r.get("model", cfg.reviewer_model)
            cfg.reviewer_strictness = r.get("strictness", cfg.reviewer_strictness)
    scopes = data.get("scopes", {})
    if isinstance(scopes, dict):
        cfg.allow_network = scopes.get("allow_network", cfg.allow_network)
        cfg.read_only_outside_target = scopes.get(
            "read_only_outside_target", cfg.read_only_outside_target
        )
    serve = data.get("serve", {})
    if isinstance(serve, dict):
        cfg.serve_host = serve.get("host", cfg.serve_host)
        cfg.serve_port = serve.get("port", cfg.serve_port)
    return cfg

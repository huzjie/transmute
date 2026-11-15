# -*- coding: utf-8 -*-
"""TransmuteClient：零依赖 Python 客户端（urllib）。"""
from __future__ import annotations

import json
import urllib.request


class TransmuteClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str):
        with urllib.request.urlopen(f"{self.base_url}{path}", timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))

    def _post(self, path: str, payload: dict):
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}{path}", data=data,
            headers={"Content-Type": "application/json"}, method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))

    def health(self) -> dict:
        return self._get("/health")

    def create_migration(self, config: str = "config.yaml") -> dict:
        return self._post("/v1/migrations", {"config": config})

    def get_migration(self, job_id: str) -> dict:
        return self._get(f"/v1/migrations/{job_id}")

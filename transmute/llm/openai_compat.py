# -*- coding: utf-8 -*-
"""OpenAI 兼容 provider（任意 /v1/chat/completions 端点，零依赖 urllib）。"""
from __future__ import annotations

import json
import urllib.request

from .base import LLMProvider, LLMResult


class OpenAICompatProvider(LLMProvider):
    name = "openai_compat"

    def __init__(self, model, temperature=0.2, api_key="", base_url="", **kw):
        super().__init__(model, temperature, api_key, **kw)
        self.base_url = (base_url or "http://localhost:11434/v1").rstrip("/")

    def _post(self, payload: dict) -> LLMResult:
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions", data=data, headers=headers, method="POST"
        )
        with urllib.request.urlopen(req, timeout=120) as r:
            body = json.loads(r.read().decode("utf-8"))
        text = body["choices"][0]["message"]["content"]
        usage = body.get("usage")
        return LLMResult(text=text, raw=body, usage=usage)

    def complete(self, prompt, system=""):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return self._post({
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        })

    def chat(self, messages, temperature=None):
        return self._post({
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature if temperature is None else temperature,
        })


from .registry import register  # noqa: E402

register(OpenAICompatProvider)

# -*- coding: utf-8 -*-
"""Anthropic Messages API provider。"""
from __future__ import annotations

import json
import urllib.request

from .base import LLMProvider, LLMResult


class AnthropicProvider(LLMProvider):
    name = "anthropic"

    def __init__(self, model, temperature=0.2, api_key="", **kw):
        super().__init__(model, temperature, api_key, **kw)

    def _post(self, payload: dict) -> LLMResult:
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages", data=data, headers=headers, method="POST"
        )
        with urllib.request.urlopen(req, timeout=180) as r:
            body = json.loads(r.read().decode("utf-8"))
        text = "".join(block.get("text", "") for block in body.get("content", []))
        return LLMResult(text=text, raw=body, usage=body.get("usage"))

    def complete(self, prompt, system=""):
        return self._post({
            "model": self.model,
            "max_tokens": 8192,
            "temperature": self.temperature,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        })

    def chat(self, messages, temperature=None):
        sys_msg = ""
        rest = []
        for m in messages:
            if m.get("role") == "system":
                sys_msg = m.get("content", "")
            else:
                rest.append(m)
        return self._post({
            "model": self.model,
            "max_tokens": 8192,
            "temperature": self.temperature if temperature is None else temperature,
            "system": sys_msg,
            "messages": rest,
        })


from .registry import register  # noqa: E402

register(AnthropicProvider)

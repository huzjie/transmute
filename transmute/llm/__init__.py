"""LLM 适配层。"""
from .base import LLMProvider, LLMResult
from .registry import get_provider, list_providers

__all__ = ["LLMProvider", "LLMResult", "get_provider", "list_providers"]

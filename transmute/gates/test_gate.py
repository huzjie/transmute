# -*- coding: utf-8 -*-
"""单元测试门禁：目标模块测试全绿才算过（正确性的唯一真值）。"""
from .base import Gate


class TestGate(Gate):
    name = "test"

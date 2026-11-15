# -*- coding: utf-8 -*-
import pytest

from transmute._core import RNG, seed_from, md5_short
from transmute.config import Config, load_config


def test_seed_deterministic():
    assert seed_from("mutex.cc") == seed_from("mutex.cc")
    assert seed_from("mutex.cc") != seed_from("mutex.h")


def test_rng_reproducible():
    r1, r2 = RNG("abc"), RNG("abc")
    assert [r1.randint(1, 100) for _ in range(5)] == [r2.randint(1, 100) for _ in range(5)]


def test_md5_short():
    assert len(md5_short(b"hello")) == 12


def test_config_defaults():
    cfg = load_config(None)
    assert cfg.llm_provider == "mock"
    assert cfg.source_lang == "cpp"
    assert cfg.target_lang == "rust"

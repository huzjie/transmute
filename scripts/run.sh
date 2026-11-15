#!/usr/bin/env bash
set -euo pipefail
# 跑完整迁移
python -m transmute.cli.main run --config "${1:-config.yaml}"

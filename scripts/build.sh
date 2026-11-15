#!/usr/bin/env bash
set -euo pipefail
# 构建 wheel
pip install build
python -m build

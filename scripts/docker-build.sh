#!/usr/bin/env bash
set -euo pipefail
docker build -f deploy/Dockerfile -t huzjie/transmute:0.1.0 .

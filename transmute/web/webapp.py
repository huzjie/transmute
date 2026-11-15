# -*- coding: utf-8 -*-
"""Web 控制台：单文件内嵌 HTML 仪表盘（无外部依赖）。"""
from __future__ import annotations

import http.server
import json
import os
import webbrowser
from pathlib import Path

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>transmute 控制台</title>
<style>
  body { font-family: "Microsoft YaHei", sans-serif; margin: 0; background: #f5f6f8; color: #1f2329; }
  header { background: #e60012; color: #fff; padding: 18px 28px; font-size: 20px; font-weight: 700; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; padding: 24px; }
  .card { background: #fff; border-radius: 6px; padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
  .card h3 { margin: 0 0 10px; font-size: 14px; color: #888; }
  .card .num { font-size: 30px; font-weight: 700; color: #e60012; }
  .flow { padding: 0 24px 24px; }
  .step { display: inline-block; background: #fff; border: 1px solid #e5e6eb; padding: 10px 16px; margin-right: 8px; border-radius: 4px; }
  .arrow { color: #e60012; margin: 0 4px; }
</style>
</head>
<body>
<header>transmute — 多智能体验证式代码迁移编排引擎</header>
<div class="grid">
  <div class="card"><h3>子任务总数</h3><div class="num" id="total">-</div></div>
  <div class="card"><h3>已合并</h3><div class="num" id="merged">-</div></div>
  <div class="card"><h3>复核通过</h3><div class="num" id="reviewed">-</div></div>
  <div class="card"><h3>失败</h3><div class="num" id="failed">-</div></div>
</div>
<div class="flow">
  <span class="step">任务切分</span><span class="arrow">→</span>
  <span class="step">候选生成</span><span class="arrow">→</span>
  <span class="step">测试门禁</span><span class="arrow">→</span>
  <span class="step">双智能体复核</span><span class="arrow">→</span>
  <span class="step">合并/回滚</span>
</div>
<script>
async function refresh() {
  try {
    const r = await fetch("/api/summary");
    const d = await r.json();
    document.getElementById("total").textContent = d.total ?? "-";
    document.getElementById("merged").textContent = d.merged ?? "-";
    document.getElementById("reviewed").textContent = d.reviewed ?? "-";
    document.getElementById("failed").textContent = d.failed ?? "-";
  } catch (e) {}
}
refresh();
setInterval(refresh, 3000);
</script>
</body>
</html>
"""


def _summary() -> dict:
    plan_path = Path("migration.plan.json")
    if not plan_path.exists():
        return {"total": 0, "merged": 0, "reviewed": 0, "failed": 0}
    from ..core.plan import MigrationPlan
    plan = MigrationPlan.load(str(plan_path))
    return {
        "total": len(plan.tasks),
        "merged": sum(1 for t in plan.tasks if t.status.value == "merged"),
        "reviewed": sum(1 for t in plan.tasks if t.status.value == "reviewed"),
        "failed": sum(1 for t in plan.tasks if t.status.value in ("failed", "rejected")),
    }


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/summary":
            body = json.dumps(_summary()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        body = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def serve(host: str = "127.0.0.1", port: int = 8001, open_browser: bool = True):
    if open_browser:
        import threading
        threading.Timer(0.6, lambda: webbrowser.open(f"http://{host}:{port}")).start()
    httpd = http.server.HTTPServer((host, port), Handler)
    print(f"transmute 控制台: http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    serve()

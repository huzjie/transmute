# Docker

多阶段构建：build 阶段装依赖，运行时阶段拷贝 site-packages，镜像更小。

```bash
docker build -f deploy/Dockerfile -t huzjie/transmute:0.1.0 .
docker compose -f deploy/docker-compose.yml up
```

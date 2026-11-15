# 服务

FastAPI 起服务：

- `/health` 健康检查
- `POST /v1/migrations` 提交迁移
- `GET /v1/migrations/{id}` 查状态

默认绑定 127.0.0.1，公网部署请加鉴权。

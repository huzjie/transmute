# 多阶段构建：编译最小化 + 运行时
FROM python:3.11-slim AS build
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir . ".[serve]"

FROM python:3.11-slim
WORKDIR /app
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin/transmute /usr/local/bin/transmute
COPY . .
EXPOSE 8000
ENV TM_LOG_LEVEL=INFO
CMD ["python", "-m", "transmute.cli.main", "doctor"]

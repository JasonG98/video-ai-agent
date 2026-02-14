# 爆款视频AI复刻引擎（video_ai_agent）

一个可运行、可扩展的 MVP：上传视频 -> Celery 异步分析 -> 生成改编脚本。

## 技术栈
- FastAPI + SQLAlchemy 2.0 + Alembic
- PostgreSQL 15, Redis 7, Celery 5
- MinIO(S3) + local fallback
- 四层 Agent：Perception / Understanding / Reasoning / Generation

## 一键启动
```bash
docker compose up -d --build
cp .env.example .env
```

## WebUI
- 启动后访问 `http://localhost:8000/`
- 页面内可直接完成：上传视频 -> 触发分析 -> 获取分析结果 -> 触发改编 -> 查询改编结果
- API 文档仍可通过 `http://localhost:8000/docs` 访问

## 本地 `fastapi dev` 调试
- 先启动依赖服务：`docker compose up -d db redis minio`
- 再启动 API：`fastapi dev app/main.py`
- 开发环境下（`APP_ENV=dev`）会自动把 `.env` 里的 `db/redis/minio` 主机名映射为 `127.0.0.1`

## 迁移数据库
```bash
docker compose exec api alembic upgrade head
```

## 创建 MinIO bucket
```bash
# 方式1：进入 MinIO Console http://localhost:9001 手动创建 videos
# 方式2：使用 awscli/mc
```

## API 示例
### 1) 上传视频
```bash
curl -X POST "http://localhost:8000/api/v1/videos/upload" \
  -F "file=@demo.mp4"
```

### 2) 触发分析
```bash
curl -X POST "http://localhost:8000/api/v1/analysis/1/run"
```

### 3) 查询分析状态
```bash
curl "http://localhost:8000/api/v1/analysis/1/status"
```

### 4) 获取分析结果
```bash
curl "http://localhost:8000/api/v1/analysis/1/result"
```

### 5) 触发改编
```bash
curl -X POST "http://localhost:8000/api/v1/adaptation/1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "美妆",
    "name": "轻透粉底液",
    "selling_points": ["12小时持妆", "不闷痘"],
    "brand_tone": "专业可信"
  }'
```

### 6) 查询改编结果
```bash
curl "http://localhost:8000/api/v1/adaptation/1"
```

## 架构说明
- API 层只做参数校验和任务入队
- Celery task 在 `app/tasks/`，调用 service
- Service 层协调 DB / 缓存 / Agent
- Agent 层接口固定，便于替换真实模型

## 测试
```bash
pytest -q
```

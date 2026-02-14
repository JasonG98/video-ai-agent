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

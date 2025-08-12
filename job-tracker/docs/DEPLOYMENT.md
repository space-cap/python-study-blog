# Job Tracker 배포 가이드

이 가이드는 Job Tracker 애플리케이션을 프로덕션 환경에 배포하는 방법을 설명합니다.

## 목차
- [Docker를 사용한 컨테이너화](#docker를-사용한-컨테이너화)
- [프로덕션 환경 설정](#프로덕션-환경-설정)
- [환경변수 관리](#환경변수-관리)
- [데이터베이스 마이그레이션](#데이터베이스-마이그레이션)
- [로그 관리](#로그-관리)
- [성능 모니터링](#성능-모니터링)
- [백업 및 복구](#백업-및-복구)

## Docker를 사용한 컨테이너화

### Dockerfile

프로젝트 루트에 `Dockerfile`을 생성하세요:

```dockerfile
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 데이터베이스 디렉토리 생성
RUN mkdir -p /app/database

# 포트 노출
EXPOSE 8000

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  job-tracker:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./database/job_tracker.db
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - API_DEBUG=false
    volumes:
      - ./database:/app/database
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - job-tracker
    restart: unless-stopped

volumes:
  database_data:
  logs_data:
```

### 프로덕션용 docker-compose.prod.yml

```yaml
version: '3.8'

services:
  job-tracker:
    build:
      context: .
      dockerfile: Dockerfile.prod
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - API_DEBUG=false
      - SCRAPY_LOG_LEVEL=WARNING
    volumes:
      - database_data:/app/database
      - logs_data:/app/logs
    restart: unless-stopped
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - logs_data:/var/log/nginx
    depends_on:
      - job-tracker
    restart: unless-stopped

volumes:
  database_data:
  logs_data:
  redis_data:
```

### 빌드 및 실행

```bash
# 개발 환경
docker-compose up -d

# 프로덕션 환경
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 프로덕션 환경 설정

### Nginx 설정 (nginx.conf)

```nginx
events {
    worker_connections 1024;
}

http {
    upstream job_tracker {
        server job-tracker:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://job_tracker;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://job_tracker/;
            access_log off;
        }

        # Static files (if any)
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### Gunicorn을 사용한 프로덕션 실행

```bash
# gunicorn 설치
pip install gunicorn

# gunicorn.conf.py 생성
```

```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
keepalive = 2
timeout = 30
graceful_timeout = 30

# Logging
accesslog = "/app/logs/access.log"
errorlog = "/app/logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
```

## 환경변수 관리

### .env.prod 파일 생성

```bash
# 데이터베이스 설정
DATABASE_URL=sqlite:///./database/job_tracker.db

# API 설정
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false

# Scrapy 설정
SCRAPY_LOG_LEVEL=WARNING
SCRAPY_USER_AGENT=job-tracker-prod (+https://your-domain.com)

# 크롤링 설정
SARAMIN_DELAY=2
CONCURRENT_REQUESTS=1
CONCURRENT_REQUESTS_PER_DOMAIN=1

# 보안 설정
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# 모니터링
SENTRY_DSN=your-sentry-dsn
```

### 환경변수 주입

```bash
# Docker Compose에서
docker-compose --env-file .env.prod up -d

# Kubernetes에서
kubectl create secret generic job-tracker-env --from-env-file=.env.prod
```

## 데이터베이스 마이그레이션

### Alembic 설정

```bash
# alembic 초기화
alembic init alembic

# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 실행
alembic upgrade head
```

### alembic.ini 설정

```ini
[alembic]
script_location = alembic
sqlalchemy.url = driver://user:pass@localhost/dbname

[post_write_hooks]
hooks = black
black.type = console_scripts
black.entrypoint = black
black.options = -l 79 REVISION_SCRIPT_FILENAME
```

### 배포시 마이그레이션 자동화

```bash
#!/bin/bash
# deploy.sh

echo "Starting deployment..."

# 애플리케이션 중지
docker-compose down

# 최신 코드 가져오기
git pull origin main

# 데이터베이스 백업
cp database/job_tracker.db database/job_tracker_backup_$(date +%Y%m%d_%H%M%S).db

# 마이그레이션 실행
docker-compose run --rm job-tracker alembic upgrade head

# 애플리케이션 시작
docker-compose up -d

echo "Deployment completed!"
```

## 로그 관리

### 구조화된 로깅 설정

```python
# config/logging.py
import logging
import sys
from pathlib import Path

def setup_logging():
    # 로그 디렉토리 생성
    log_dir = Path("/app/logs")
    log_dir.mkdir(exist_ok=True)
    
    # 포맷터 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 파일 핸들러
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger
```

### 로그 로테이션 (logrotate)

```bash
# /etc/logrotate.d/job-tracker
/app/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        docker-compose exec job-tracker kill -USR1 1
    endscript
}
```

### ELK Stack 연동

```yaml
# docker-compose.logging.yml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.5.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.5.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  elasticsearch_data:
```

## 성능 모니터링

### Prometheus + Grafana 설정

```yaml
# docker-compose.monitoring.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"

volumes:
  prometheus_data:
  grafana_data:
```

### 애플리케이션 메트릭스

```python
# main.py에 추가
from prometheus_client import Counter, Histogram, generate_latest
import time

# 메트릭스 정의
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

@app.middleware("http")
async def add_metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()
    
    REQUEST_LATENCY.observe(time.time() - start_time)
    
    return response

@app.get("/metrics")
async def get_metrics():
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

### 헬스체크 엔드포인트

```python
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # 데이터베이스 연결 확인
        db.execute("SELECT 1")
        return {"status": "healthy", "timestamp": datetime.utcnow()}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Database connection failed")

@app.get("/ready")
async def readiness_check():
    # 애플리케이션 준비 상태 확인
    return {"status": "ready"}
```

## 백업 및 복구

### 데이터베이스 백업 스크립트

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/app/backups"
DB_FILE="/app/database/job_tracker.db"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/job_tracker_$DATE.db"

# 백업 디렉토리 생성
mkdir -p $BACKUP_DIR

# 데이터베이스 백업
cp $DB_FILE $BACKUP_FILE

# 압축
gzip $BACKUP_FILE

# 7일 이상 된 백업 파일 삭제
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: ${BACKUP_FILE}.gz"
```

### 자동 백업 (Crontab)

```bash
# crontab -e
# 매일 새벽 2시에 백업 실행
0 2 * * * /app/scripts/backup.sh

# 매주 일요일 새벽 3시에 주간 백업
0 3 * * 0 /app/scripts/weekly_backup.sh
```

### 복구 절차

```bash
#!/bin/bash
# restore.sh

BACKUP_FILE=$1
DB_FILE="/app/database/job_tracker.db"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

echo "Stopping application..."
docker-compose down

echo "Restoring database from $BACKUP_FILE..."

# 현재 데이터베이스 백업
cp $DB_FILE "${DB_FILE}.before_restore"

# 백업 파일 압축 해제 및 복원
gunzip -c $BACKUP_FILE > $DB_FILE

echo "Starting application..."
docker-compose up -d

echo "Restore completed!"
```

### AWS S3 백업

```python
# backup_s3.py
import boto3
import os
from datetime import datetime

def upload_to_s3():
    s3 = boto3.client('s3')
    bucket_name = os.getenv('S3_BUCKET_NAME')
    
    local_file = '/app/database/job_tracker.db'
    s3_key = f'backups/job_tracker_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
    
    try:
        s3.upload_file(local_file, bucket_name, s3_key)
        print(f"Backup uploaded to S3: {s3_key}")
    except Exception as e:
        print(f"S3 upload failed: {e}")

if __name__ == "__main__":
    upload_to_s3()
```

## 배포 체크리스트

### 배포 전 점검사항

- [ ] 환경변수 설정 확인
- [ ] 데이터베이스 마이그레이션 테스트
- [ ] SSL 인증서 설정
- [ ] 방화벽 규칙 설정
- [ ] 백업 시스템 동작 확인
- [ ] 모니터링 시스템 연동
- [ ] 헬스체크 엔드포인트 동작 확인

### 배포 후 점검사항

- [ ] 애플리케이션 정상 동작 확인
- [ ] API 엔드포인트 테스트
- [ ] 로그 수집 정상 동작 확인
- [ ] 메트릭 수집 정상 동작 확인
- [ ] 백업 자동화 동작 확인
- [ ] 성능 모니터링 알림 설정

## 문제 해결

### 일반적인 문제들

1. **컨테이너 시작 실패**
   ```bash
   docker-compose logs job-tracker
   ```

2. **데이터베이스 연결 오류**
   ```bash
   # 권한 확인
   ls -la database/
   # 데이터베이스 파일 복구
   ./scripts/restore.sh backups/latest_backup.db.gz
   ```

3. **메모리 부족**
   ```bash
   # 리소스 사용량 확인
   docker stats
   # 메모리 제한 조정
   # docker-compose.yml의 deploy.resources 섹션 수정
   ```

### 긴급 대응 절차

1. **서비스 중단 시**
   - 즉시 이전 버전으로 롤백
   - 로그 확인 및 문제 원인 파악
   - 핫픽스 준비 및 테스트

2. **데이터 손실 시**
   - 즉시 서비스 중단
   - 최신 백업으로 복구
   - 데이터 정합성 검증

이 가이드를 통해 Job Tracker 애플리케이션을 안전하고 효율적으로 프로덕션 환경에 배포할 수 있습니다.
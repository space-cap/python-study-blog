# Job Tracker

사람인(Saramin) 채용사이트를 크롤링하여 채용공고를 수집하고 관리하는 웹 애플리케이션입니다.

## 🚀 주요 기능

- **채용공고 크롤링**: 사람인 웹사이트에서 채용공고 자동 수집
- **채용공고 관리**: 수집된 채용공고 조회, 삭제 기능
- **RESTful API**: FastAPI 기반의 REST API 제공
- **데이터베이스 저장**: SQLite를 통한 채용공고 영구 저장
- **백그라운드 처리**: 비동기 크롤링 작업 지원

## 🛠 기술 스택

### Backend
- **FastAPI** (0.104.1) - 웹 API 프레임워크
- **SQLAlchemy** (2.0.23) - ORM 및 데이터베이스 관리
- **Uvicorn** (0.24.0) - ASGI 서버

### Web Scraping
- **Scrapy** (2.11.0) - 웹 크롤링 프레임워크
- **scrapy-user-agents** - 다양한 User-Agent 사용
- **scrapy-rotating-proxies** - 프록시 로테이션

### Database
- **SQLite** - 로컬 데이터베이스
- **Alembic** - 데이터베이스 마이그레이션

### Development Tools
- **pytest** - 테스트 프레임워크
- **black** - 코드 포매터
- **isort** - import 정렬
- **flake8** - 린팅

## 📦 설치 및 실행

### 1. 프로젝트 클론 및 가상환경 설정

```bash
git clone <repository-url>
cd job-tracker

# 가상환경 생성 및 활성화
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

```bash
python main.py
```

서버는 `http://localhost:8000`에서 실행됩니다.

## 📡 API 엔드포인트

### 기본 정보
- **Base URL**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)

### 주요 엔드포인트

#### 1. 루트 엔드포인트
```http
GET /
```
API 환영 메시지 반환

#### 2. 크롤링 실행
```http
POST /api/jobs/crawl
Content-Type: application/json

{
  "url": "https://www.saramin.co.kr/..."
}
```

#### 3. 채용공고 목록 조회
```http
GET /api/jobs?skip=0&limit=100
```

#### 4. 채용공고 상세 조회
```http
GET /api/jobs/{job_id}
```

#### 5. 채용공고 삭제
```http
DELETE /api/jobs/{job_id}
```

#### 6. 크롤링 실행 (단순)
```http
POST /scrape/
```

### 레거시 엔드포인트 (하위 호환성)
```http
GET /jobs/          # 채용공고 목록
POST /jobs/         # 새 채용공고 생성
```

## 💡 사용 예시

### 1. 크롤링 실행
```bash
curl -X POST "http://localhost:8000/api/jobs/crawl" \
-H "Content-Type: application/json" \
-d '{"url": "https://www.saramin.co.kr/zf_user/search/recruit?searchword=개발자"}'
```

### 2. 채용공고 조회
```bash
curl "http://localhost:8000/api/jobs?limit=10"
```

### 3. 특정 채용공고 조회
```bash
curl "http://localhost:8000/api/jobs/1"
```

## 📁 프로젝트 구조

```
job-tracker/
├── app/                    # FastAPI 애플리케이션
│   ├── __init__.py
│   ├── crud.py            # 데이터베이스 CRUD 연산
│   ├── database.py        # 데이터베이스 연결 설정
│   ├── models.py          # SQLAlchemy 모델
│   └── schemas.py         # Pydantic 스키마
├── config/                # 설정 파일
│   ├── __init__.py
│   └── settings.py
├── scrapy_project/        # Scrapy 크롤링 프로젝트
│   ├── __init__.py
│   ├── items.py          # Scrapy 아이템 정의
│   ├── pipelines.py      # 데이터 처리 파이프라인
│   ├── runner.py         # Scrapy 실행 함수
│   ├── settings.py       # Scrapy 설정
│   └── spiders/          # 크롤링 스파이더
│       ├── __init__.py
│       └── saramin_spider.py
├── database/             # 데이터베이스 관련 파일
├── tests/               # 테스트 파일
├── main.py             # FastAPI 애플리케이션 메인 파일
├── requirements.txt    # Python 의존성
├── scrapy.cfg         # Scrapy 설정 파일
└── job_tracker.db     # SQLite 데이터베이스 파일
```

## ⚠️ 주의사항 및 크롤링 윤리

### 크롤링 윤리 준수
- **robots.txt 확인**: 크롤링 전 대상 웹사이트의 robots.txt를 확인하고 준수
- **요청 간격**: 서버 부하 방지를 위한 적절한 딜레이 설정 (현재 2초)
- **동시 요청 제한**: 동시 요청 수를 제한하여 서버에 무리를 주지 않음
- **개인정보 보호**: 개인정보나 민감한 정보는 수집하지 않음

### 현재 설정된 크롤링 제한
```python
custom_settings = {
    'DOWNLOAD_DELAY': 2,                    # 요청 간 2초 대기
    'CONCURRENT_REQUESTS': 1,               # 전체 동시 요청 1개
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,    # 도메인당 동시 요청 1개
}
```

### 법적 고지
- 본 도구는 **교육 및 연구 목적**으로만 사용해야 합니다
- 상업적 이용 시 해당 웹사이트의 이용약관을 반드시 확인하세요
- 대량 크롤링이나 과도한 요청은 피해주세요
- 저작권 및 개인정보보호법을 준수하세요

### 기술적 권장사항
- 프로덕션 환경에서는 PostgreSQL 등의 데이터베이스 사용 권장
- 크롤링 작업은 별도 큐 시스템(Celery 등) 사용 권장
- 로그 관리 시스템 도입 권장
- API 인증 및 권한 관리 구현 권장

## 📄 라이센스

이 프로젝트는 교육 목적으로 제작되었습니다. 사용 시 관련 법률과 웹사이트 이용약관을 준수해 주세요.

## 🤝 기여

버그 리포트나 기능 제안은 이슈를 통해 알려주세요.

---

**⚠️ 면책조항**: 이 도구를 사용하여 발생하는 모든 법적 책임은 사용자에게 있습니다. 웹사이트의 robots.txt와 이용약관을 반드시 확인하고 준수하세요.
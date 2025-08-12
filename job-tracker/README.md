# Job Tracker

사람인 잡사이트 크롤링 및 채용정보 추적을 위한 FastAPI + Scrapy 프로젝트

## 기능

- 사람인 채용정보 크롤링
- 추출 데이터: 기업명, 시작일, 마감일, 지원자수, 자격요건, 우대사항, 지역
- SQLite 데이터베이스 저장
- FastAPI REST API 제공

## 설치 및 실행

### 1. 가상환경 설정

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경설정

`.env` 파일을 확인하고 필요시 수정

### 4. 서버 실행

```bash
python main.py
```

API 문서: http://localhost:8000/docs

### 5. 크롤링 실행

```bash
# 직접 Scrapy 실행
cd scrapy_project
scrapy crawl saramin

# 또는 API를 통한 크롤링
curl -X POST "http://localhost:8000/scrape/"
```

## API 엔드포인트

- `GET /`: 메인페이지
- `GET /jobs/`: 채용정보 목록 조회
- `POST /jobs/`: 채용정보 생성
- `POST /scrape/`: 크롤링 시작

## 프로젝트 구조

```
job-tracker/
├── app/                    # FastAPI 앱
│   ├── __init__.py
│   ├── database.py         # 데이터베이스 설정
│   ├── models.py           # SQLAlchemy 모델
│   ├── schemas.py          # Pydantic 스키마
│   └── crud.py             # CRUD 기능
├── scrapy_project/         # Scrapy 프로젝트
│   ├── spiders/
│   │   └── saramin_spider.py
│   ├── items.py
│   ├── pipelines.py
│   ├── settings.py
│   └── runner.py
├── config/                 # 설정 파일
│   ├── __init__.py
│   └── settings.py
├── .env                    # 환경변수
├── main.py                 # FastAPI 메인 앱
├── requirements.txt        # 의존성
└── README.md
```

## 주의사항

- 웹 크롤링 시 사이트의 robots.txt와 이용약관을 준수하세요
- 과도한 요청으로 서버에 부하를 주지 않도록 딜레이를 설정했습니다
- 실제 운영환경에서는 더 강력한 데이터베이스(PostgreSQL 등)를 사용하는 것을 권장합니다
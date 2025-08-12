# Job Tracker 개발자 가이드

이 문서는 Job Tracker 프로젝트의 개발자를 위한 종합적인 가이드입니다.

## 목차

1. [프로젝트 구조](#프로젝트-구조)
2. [각 모듈별 역할과 책임](#각-모듈별-역할과-책임)
3. [새로운 크롤러 추가 방법](#새로운-크롤러-추가-방법)
4. [데이터베이스 스키마 변경 방법](#데이터베이스-스키마-변경-방법)
5. [테스트 작성 및 실행](#테스트-작성-및-실행)
6. [코드 스타일 가이드](#코드-스타일-가이드)
7. [개발 환경 설정](#개발-환경-설정)
8. [디버깅 가이드](#디버깅-가이드)

## 프로젝트 구조

```
job-tracker/
├── app/                      # FastAPI 웹 애플리케이션
│   ├── __init__.py          
│   ├── crud.py              # 데이터베이스 CRUD 연산
│   ├── database.py          # 데이터베이스 연결 및 세션 관리
│   ├── models.py            # SQLAlchemy ORM 모델
│   └── schemas.py           # Pydantic 스키마 (API 입출력 모델)
├── config/                   # 애플리케이션 설정
│   ├── __init__.py
│   └── settings.py          # 환경별 설정 관리
├── scrapy_project/          # Scrapy 웹 크롤링 프로젝트
│   ├── __init__.py
│   ├── items.py             # Scrapy 아이템 정의 (크롤링 데이터 구조)
│   ├── items/               # 아이템 관련 확장 모듈
│   ├── pipelines.py         # 데이터 처리 파이프라인
│   ├── pipelines/           # 파이프라인 확장 모듈
│   ├── runner.py            # Scrapy 스파이더 실행 함수
│   ├── settings.py          # Scrapy 프레임워크 설정
│   └── spiders/             # 웹사이트별 크롤링 스파이더
│       ├── __init__.py
│       └── saramin_spider.py # 사람인 웹사이트 크롤러
├── database/                # 데이터베이스 관련 파일 (마이그레이션 등)
├── docs/                    # 프로젝트 문서
│   ├── API.md              # API 문서
│   ├── INSTALLATION.md     # 설치 가이드
│   ├── DEVELOPMENT.md      # 개발자 가이드 (이 파일)
│   └── CONTRIBUTING.md     # 기여 가이드
├── tests/                   # 테스트 코드
├── main.py                  # FastAPI 애플리케이션 진입점
├── requirements.txt         # Python 의존성 패키지 목록
├── scrapy.cfg              # Scrapy 프로젝트 설정 파일
└── job_tracker.db          # SQLite 데이터베이스 파일
```

## 각 모듈별 역할과 책임

### 1. `app/` 모듈 - FastAPI 웹 애플리케이션

#### `app/models.py`
- **역할**: SQLAlchemy ORM 모델 정의
- **책임**: 데이터베이스 테이블 구조 정의 및 관계 설정
- **주요 클래스**: 
  - `JobPosting`: 채용공고 데이터 모델

```python
# 예시: JobPosting 모델 구조
class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    # ... 기타 필드들
```

#### `app/schemas.py`
- **역할**: Pydantic 스키마 정의 (API 입출력 검증)
- **책임**: API 요청/응답 데이터 구조 정의 및 검증
- **주요 클래스**:
  - `JobPostingCreate`: 채용공고 생성 스키마
  - `JobPosting`: 채용공고 응답 스키마
  - `CrawlRequest`: 크롤링 요청 스키마

#### `app/crud.py`
- **역할**: 데이터베이스 CRUD 연산 추상화
- **책임**: 데이터베이스 쿼리 로직 집중화
- **주요 함수**:
  - `get_job_postings()`: 채용공고 목록 조회
  - `get_job_posting()`: 특정 채용공고 조회
  - `create_job_posting()`: 채용공고 생성
  - `delete_job_posting()`: 채용공고 삭제

#### `app/database.py`
- **역할**: 데이터베이스 연결 및 세션 관리
- **책임**: SQLAlchemy 엔진 설정, 세션 생성 및 관리
- **주요 요소**:
  - 데이터베이스 URL 설정
  - 세션 팩토리 생성
  - 의존성 주입을 위한 `get_db()` 함수

### 2. `scrapy_project/` 모듈 - 웹 크롤링

#### `spiders/saramin_spider.py`
- **역할**: 사람인 웹사이트 크롤링 로직
- **책임**: 웹 페이지 파싱, 데이터 추출
- **주요 메서드**:
  - `start_requests()`: 초기 요청 생성
  - `parse()`: 검색 결과 페이지 파싱
  - `parse_job_detail()`: 채용공고 상세 페이지 파싱

#### `items.py`
- **역할**: 크롤링된 데이터 구조 정의
- **책임**: Scrapy 아이템 필드 정의
- **주요 클래스**: `JobPostingItem`

#### `pipelines.py`
- **역할**: 크롤링된 데이터 후처리
- **책임**: 데이터 검증, 변환, 저장
- **주요 클래스**: `DatabasePipeline`

#### `runner.py`
- **역할**: Scrapy 스파이더 실행 인터페이스
- **책임**: FastAPI에서 Scrapy 스파이더를 실행할 수 있게 하는 브리지

### 3. `main.py` - 애플리케이션 진입점
- **역할**: FastAPI 애플리케이션 설정 및 라우팅
- **책임**: API 엔드포인트 정의, 미들웨어 설정

## 새로운 크롤러 추가 방법

새로운 웹사이트의 크롤러를 추가하는 단계별 가이드입니다.

### 1단계: 새 스파이더 파일 생성

```bash
# scrapy_project/spiders/ 디렉토리에 새 스파이더 파일 생성
touch scrapy_project/spiders/new_site_spider.py
```

### 2단계: 스파이더 클래스 구현

```python
# scrapy_project/spiders/new_site_spider.py
import scrapy
from datetime import datetime
from scrapy_project.items import JobPostingItem

class NewSiteSpider(scrapy.Spider):
    name = 'new_site'  # 고유한 스파이더 이름
    allowed_domains = ['example.com']  # 허용된 도메인
    
    # 크롤링 설정
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # 요청 간 지연 시간
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    }
    
    def start_requests(self):
        """초기 요청 URL 설정"""
        urls = [
            'https://example.com/jobs',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        """메인 페이지 파싱 로직"""
        # 채용공고 링크 추출
        job_links = response.css('.job-link::attr(href)').getall()
        
        for link in job_links:
            full_url = response.urljoin(link)
            yield scrapy.Request(url=full_url, callback=self.parse_job_detail)
    
    def parse_job_detail(self, response):
        """채용공고 상세 정보 추출"""
        item = JobPostingItem()
        
        # 각 필드에 맞는 CSS 선택자 또는 XPath 사용
        item['company_name'] = response.css('.company-name::text').get()
        item['job_title'] = response.css('.job-title::text').get()
        item['location'] = response.css('.location::text').get()
        # ... 기타 필드들
        
        yield item
```

### 3단계: 아이템 필드 확장 (필요시)

새로운 웹사이트에서 추가 데이터를 수집해야 하는 경우:

```python
# scrapy_project/items.py에 필드 추가
class JobPostingItem(scrapy.Item):
    # 기존 필드들...
    new_field = scrapy.Field()  # 새로운 필드 추가
```

### 4단계: 데이터베이스 모델 업데이트 (필요시)

```python
# app/models.py에 컬럼 추가
class JobPosting(Base):
    # 기존 컬럼들...
    new_column = Column(String(255))  # 새로운 컬럼 추가
```

### 5단계: 파이프라인 업데이트

```python
# scrapy_project/pipelines.py의 DatabasePipeline 수정
def process_item(self, item, spider):
    # 새로운 필드 처리 로직 추가
    job_posting = JobPosting(
        # 기존 필드들...
        new_column=item.get('new_field'),
    )
```

### 6단계: 스파이더 테스트

```bash
# 새 스파이더 테스트 실행
cd scrapy_project
scrapy crawl new_site -s LOG_LEVEL=DEBUG
```

### 7단계: runner.py에 스파이더 추가

```python
# scrapy_project/runner.py 수정
def run_spider(spider_name='saramin'):
    """지정된 스파이더 실행"""
    # 여러 스파이더를 선택할 수 있도록 수정
    if spider_name not in ['saramin', 'new_site']:
        spider_name = 'saramin'
    
    # ... 실행 로직
```

## 데이터베이스 스키마 변경 방법

데이터베이스 스키마를 안전하게 변경하는 방법입니다.

### 1단계: 모델 수정

```python
# app/models.py
class JobPosting(Base):
    __tablename__ = "job_postings"
    
    # 기존 필드들...
    
    # 새 필드 추가 예시
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    benefits = Column(Text)
```

### 2단계: 스키마 업데이트

```python
# app/schemas.py
class JobPostingCreate(BaseModel):
    # 기존 필드들...
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    benefits: Optional[str] = None

class JobPosting(JobPostingCreate):
    # 응답 스키마에도 동일하게 추가
    class Config:
        orm_mode = True
```

### 3단계: CRUD 함수 업데이트

```python
# app/crud.py
def create_job_posting(db: Session, job: schemas.JobPostingCreate):
    db_job = models.JobPosting(**job.dict())  # Pydantic 모델의 모든 필드를 포함
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
```

### 4단계: 데이터베이스 마이그레이션

현재 프로젝트는 자동 테이블 생성을 사용하지만, 프로덕션에서는 Alembic 사용을 권장:

```bash
# Alembic 설정 (선택사항)
pip install alembic
alembic init alembic

# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Add salary and benefits fields"

# 마이그레이션 적용
alembic upgrade head
```

### 5단계: 기존 데이터 호환성 확인

스키마 변경 후 기존 데이터와의 호환성을 확인:

```python
# 테스트 스크립트 예시
from app.database import get_db
from app.crud import get_job_postings

db = next(get_db())
jobs = get_job_postings(db)
print(f"기존 데이터 {len(jobs)}개 로드 성공")
```

## 테스트 작성 및 실행

### 테스트 구조

```
tests/
├── __init__.py
├── conftest.py              # pytest 설정 및 픽스처
├── test_api/               # API 테스트
│   ├── __init__.py
│   ├── test_jobs.py        # 채용공고 API 테스트
│   └── test_crawling.py    # 크롤링 API 테스트
├── test_scrapers/          # 크롤러 테스트
│   ├── __init__.py
│   └── test_saramin_spider.py
└── test_database/          # 데이터베이스 테스트
    ├── __init__.py
    └── test_crud.py
```

### API 테스트 작성 예시

```python
# tests/test_api/test_jobs.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base

# 테스트용 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

def test_get_jobs_empty(client):
    """빈 데이터베이스에서 채용공고 목록 조회 테스트"""
    response = client.get("/api/jobs")
    assert response.status_code == 200
    assert response.json() == []

def test_create_job(client):
    """채용공고 생성 테스트"""
    job_data = {
        "company_name": "테스트 회사",
        "title": "백엔드 개발자",
        "location": "서울",
    }
    response = client.post("/jobs/", json=job_data)
    assert response.status_code == 200
    assert response.json()["company_name"] == "테스트 회사"
```

### 크롤러 테스트 작성 예시

```python
# tests/test_scrapers/test_saramin_spider.py
import pytest
from scrapy.http import HtmlResponse
from scrapy_project.spiders.saramin_spider import SaraminSpider

@pytest.fixture
def spider():
    return SaraminSpider()

def test_parse_job_detail(spider):
    """채용공고 상세 페이지 파싱 테스트"""
    html_content = """
    <html>
        <div class="company_nm">테스트 회사</div>
        <div class="job_tit"><span class="job_title">개발자</span></div>
    </html>
    """
    
    response = HtmlResponse(
        url="https://example.com/job/123",
        body=html_content.encode('utf-8')
    )
    
    results = list(spider.parse_job_detail(response))
    assert len(results) == 1
    
    item = results[0]
    assert item['company_name'] == '테스트 회사'
    assert item['job_title'] == '개발자'
```

### 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/test_api/test_jobs.py

# 커버리지 리포트와 함께 실행
pytest --cov=app tests/

# 상세 출력으로 실행
pytest -v

# 특정 테스트 함수만 실행
pytest tests/test_api/test_jobs.py::test_get_jobs_empty
```

### 테스트 픽스처 설정

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

@pytest.fixture(scope="session")
def test_engine():
    """테스트용 데이터베이스 엔진"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(test_engine):
    """테스트용 데이터베이스 세션"""
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()
```

## 코드 스타일 가이드

### Python 코드 스타일

프로젝트는 다음 도구들을 사용하여 코드 품질을 관리합니다:

#### 1. Black (코드 포매터)
```bash
# 설치
pip install black

# 전체 프로젝트 포맷팅
black .

# 특정 파일 포맷팅
black app/models.py

# 체크만 하고 변경하지 않기
black --check .
```

#### 2. isort (import 정렬)
```bash
# 설치
pip install isort

# import 정렬
isort .

# Black과 호환되는 설정으로 실행
isort --profile black .
```

#### 3. flake8 (린팅)
```bash
# 설치
pip install flake8

# 린팅 실행
flake8 .

# 설정 파일 (.flake8)
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,venv,.venv
```

### 코딩 컨벤션

#### 1. 네이밍 컨벤션
- **함수/변수**: snake_case
- **클래스**: PascalCase
- **상수**: UPPER_SNAKE_CASE
- **모듈**: snake_case

```python
# 좋은 예
class JobPosting:
    def get_job_by_id(self):
        MAX_RETRY_COUNT = 3
        job_data = self.fetch_data()

# 나쁜 예
class jobPosting:
    def getJobById(self):
        maxRetryCount = 3
        jobData = self.fetchData()
```

#### 2. 문서화
모든 공개 함수와 클래스에는 docstring을 작성합니다:

```python
def get_job_postings(db: Session, skip: int = 0, limit: int = 100):
    """
    채용공고 목록을 조회합니다.
    
    Args:
        db (Session): 데이터베이스 세션
        skip (int): 건너뛸 레코드 수
        limit (int): 최대 반환할 레코드 수
        
    Returns:
        List[JobPosting]: 채용공고 목록
    """
    return db.query(models.JobPosting).offset(skip).limit(limit).all()
```

#### 3. 타입 힌트
모든 함수는 타입 힌트를 사용합니다:

```python
from typing import List, Optional
from sqlalchemy.orm import Session

def search_jobs(
    db: Session, 
    keyword: str, 
    location: Optional[str] = None
) -> List[JobPosting]:
    query = db.query(JobPosting)
    # ... 구현
    return query.all()
```

### pre-commit 설정

코드 품질을 자동으로 관리하기 위해 pre-commit 훅을 설정할 수 있습니다:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3
        
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        args: ["--profile", "black"]
        
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
```

설치 및 활성화:
```bash
pip install pre-commit
pre-commit install
```

## 개발 환경 설정

### 1. 가상환경 설정
```bash
# Python 가상환경 생성
python -m venv .venv

# 가상환경 활성화 (Windows)
.venv\Scripts\activate

# 가상환경 활성화 (Linux/Mac)
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 개발용 의존성 추가
```bash
# 개발용 패키지들을 requirements-dev.txt에 분리
pip install -r requirements-dev.txt

# requirements-dev.txt 예시:
# pytest>=7.0.0
# black>=22.0.0
# isort>=5.10.0
# flake8>=4.0.0
# coverage>=6.0.0
```

### 3. IDE 설정

#### VS Code 설정 (.vscode/settings.json)
```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true
}
```

### 4. 환경변수 관리

환경별 설정을 위한 .env 파일:

```bash
# .env.development
DATABASE_URL=sqlite:///./job_tracker_dev.db
DEBUG=True
LOG_LEVEL=DEBUG

# .env.production  
DATABASE_URL=postgresql://user:password@localhost/job_tracker
DEBUG=False
LOG_LEVEL=INFO
```

python-dotenv를 사용한 환경변수 로드:

```python
# config/settings.py
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "sqlite:///./job_tracker.db"
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## 디버깅 가이드

### 1. 로깅 설정

```python
# config/logging.py
import logging
import sys

def setup_logging(log_level: str = "INFO"):
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log")
        ]
    )

# main.py에서 로깅 초기화
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)
```

### 2. 크롤러 디버깅

```bash
# Scrapy 디버깅 모드로 실행
scrapy crawl saramin -s LOG_LEVEL=DEBUG

# 특정 URL만 테스트
scrapy shell "https://www.saramin.co.kr/..."

# 크롤링 결과를 JSON 파일로 저장
scrapy crawl saramin -o output.json
```

### 3. API 디버깅

```python
# FastAPI 디버그 모드 활성화
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        debug=True,  # 디버그 모드
        reload=True  # 자동 리로드
    )
```

### 4. 데이터베이스 디버깅

```python
# SQLAlchemy 쿼리 로깅 활성화
engine = create_engine(
    DATABASE_URL, 
    echo=True  # SQL 쿼리 로깅
)

# 데이터베이스 상태 확인 함수
def check_db_health():
    db = SessionLocal()
    try:
        # 테이블 존재 확인
        result = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = result.fetchall()
        print(f"Available tables: {tables}")
        
        # 레코드 수 확인
        count = db.query(JobPosting).count()
        print(f"Total job postings: {count}")
        
    finally:
        db.close()
```

### 5. 일반적인 문제 해결

#### 데이터베이스 연결 문제
```python
# 연결 테스트
from sqlalchemy import create_engine

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")
```

#### 크롤링 차단 문제
```python
# User-Agent 로테이션 설정
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

# 프록시 설정 (필요시)
ROTATING_PROXY_LIST_PATH = 'proxy_list.txt'
```

이 개발자 가이드를 통해 Job Tracker 프로젝트를 효율적으로 개발하고 유지보수할 수 있습니다. 추가 질문이나 개선사항이 있다면 이슈를 통해 알려주세요.
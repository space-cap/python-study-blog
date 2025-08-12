# Job Tracker API 문서

## 개요

Job Tracker API는 사람인 잡사이트에서 채용공고를 크롤링하고 관리할 수 있는 FastAPI 기반의 REST API입니다.

- **Base URL**: `http://localhost:8000`
- **API Version**: 1.0.0
- **Content-Type**: `application/json`

## Swagger UI 접속 방법

API 서버를 실행한 후 다음 URL로 접속하여 interactive API 문서를 확인할 수 있습니다:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API 엔드포인트

### 1. POST /api/jobs/crawl

사람인 잡사이트 크롤링을 시작합니다.

#### 요청

```http
POST /api/jobs/crawl
Content-Type: application/json

{
    "url": "https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=python"
}
```

#### 요청 파라미터

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| url | string | Yes | 크롤링할 사람인 검색 URL |

#### 응답

**성공 (200)**
```json
{
    "message": "크롤링이 시작되었습니다. URL: https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=python",
    "status": "started"
}
```

#### 에러 응답

**서버 오류 (500)**
```json
{
    "detail": "크롤링 시작 중 오류 발생: [상세 에러 메시지]"
}
```

---

### 2. GET /api/jobs

저장된 채용공고 목록을 조회합니다.

#### 요청

```http
GET /api/jobs?skip=0&limit=10
```

#### 쿼리 파라미터

| 필드 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| skip | integer | 0 | 건너뛸 항목 수 (페이징) |
| limit | integer | 100 | 반환할 최대 항목 수 |

#### 응답

**성공 (200)**
```json
[
    {
        "id": 1,
        "company_name": "(주)테크컴퍼니",
        "job_title": "Python 백엔드 개발자",
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "applicant_count": 15,
        "requirements": "Python, Django, PostgreSQL 경험",
        "preferred_qualifications": "AWS, Docker 경험 우대",
        "location": "서울 강남구",
        "source_url": "https://www.saramin.co.kr/zf_user/jobs/relay/view?id=123456",
        "created_at": "2024-01-15T10:30:00"
    }
]
```

#### 응답 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| id | integer | 채용공고 고유 ID |
| company_name | string | 회사명 |
| job_title | string | 채용공고 제목 |
| start_date | string \| null | 채용 시작일 |
| end_date | string \| null | 채용 마감일 |
| applicant_count | integer | 지원자 수 |
| requirements | string \| null | 필수 요구사항 |
| preferred_qualifications | string \| null | 우대사항 |
| location | string \| null | 근무지 |
| source_url | string \| null | 원본 채용공고 URL |
| created_at | string | 생성 일시 (ISO 8601) |

---

### 3. GET /api/jobs/{job_id}

특정 채용공고의 상세 정보를 조회합니다.

#### 요청

```http
GET /api/jobs/123
```

#### 경로 파라미터

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| job_id | integer | Yes | 채용공고 고유 ID |

#### 응답

**성공 (200)**
```json
{
    "id": 123,
    "company_name": "(주)테크컴퍼니",
    "job_title": "Python 백엔드 개발자",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "applicant_count": 15,
    "requirements": "Python, Django, PostgreSQL 경험",
    "preferred_qualifications": "AWS, Docker 경험 우대",
    "location": "서울 강남구",
    "source_url": "https://www.saramin.co.kr/zf_user/jobs/relay/view?id=123456",
    "created_at": "2024-01-15T10:30:00"
}
```

#### 에러 응답

**찾을 수 없음 (404)**
```json
{
    "detail": "채용공고를 찾을 수 없습니다."
}
```

---

### 4. DELETE /api/jobs/{job_id}

특정 채용공고를 삭제합니다.

#### 요청

```http
DELETE /api/jobs/123
```

#### 경로 파라미터

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| job_id | integer | Yes | 삭제할 채용공고 고유 ID |

#### 응답

**성공 (200)**
```json
{
    "message": "채용공고가 성공적으로 삭제되었습니다."
}
```

#### 에러 응답

**찾을 수 없음 (404)**
```json
{
    "detail": "채용공고를 찾을 수 없습니다."
}
```

---

## 에러 코드

| HTTP 상태 코드 | 설명 |
|----------------|------|
| 200 | 성공 |
| 404 | 리소스를 찾을 수 없음 |
| 422 | 요청 데이터 검증 실패 |
| 500 | 서버 내부 오류 |

## 사용 예제

### 1. 크롤링 시작 및 데이터 확인

```bash
# 1. 크롤링 시작
curl -X POST "http://localhost:8000/api/jobs/crawl" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=python"}'

# 2. 잠시 후 크롤링된 데이터 확인
curl "http://localhost:8000/api/jobs?limit=5"
```

### 2. 특정 채용공고 조회 및 삭제

```bash
# 특정 채용공고 조회
curl "http://localhost:8000/api/jobs/1"

# 채용공고 삭제
curl -X DELETE "http://localhost:8000/api/jobs/1"
```

## 개발 환경 설정

### API 서버 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# API 서버 실행
python main.py
```

서버가 실행되면 `http://localhost:8000`에서 API를 사용할 수 있습니다.

### 데이터베이스

- **Type**: SQLite
- **File**: `job_tracker.db`
- **Location**: 프로젝트 루트 디렉토리

## 참고사항

- 크롤링은 백그라운드에서 실행되므로 `/api/jobs/crawl` 호출 후 바로 데이터가 나타나지 않을 수 있습니다.
- 크롤링 진행 상황은 서버 콘솔 로그에서 확인할 수 있습니다.
- 모든 시간은 ISO 8601 형식으로 반환됩니다.
- 페이징을 위해 `skip`과 `limit` 파라미터를 사용하세요.
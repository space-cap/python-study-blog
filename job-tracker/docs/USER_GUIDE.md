# Job Tracker 사용자 매뉴얼

Job Tracker는 채용 사이트(현재 사람인)에서 채용공고를 자동으로 수집하고 관리할 수 있는 웹 애플리케이션입니다. 이 매뉴얼은 최종 사용자가 시스템을 효과적으로 활용할 수 있도록 도와드립니다.

## 📋 목차
1. [웹 인터페이스 사용법](#1-웹-인터페이스-사용법)
2. [잡사이트 URL 등록 방법](#2-잡사이트-url-등록-방법)
3. [크롤링 결과 확인](#3-크롤링-결과-확인)
4. [데이터 필터링 및 검색](#4-데이터-필터링-및-검색)
5. [지원 이력 관리 팁](#5-지원-이력-관리-팁)
6. [자주 묻는 질문 (FAQ)](#6-자주-묻는-질문-faq)
7. [지원되는 사이트 목록](#7-지원되는-사이트-목록)

---

## 1. 웹 인터페이스 사용법

### 1.1 시스템 접속
- **기본 주소**: `http://localhost:8000`
- **API 문서**: `http://localhost:8000/docs` (Swagger UI)

### 1.2 주요 화면 구성
Job Tracker는 RESTful API 기반으로 작동하므로, 다음과 같은 방법으로 사용할 수 있습니다:

#### API 문서 화면 (Swagger UI)
- `http://localhost:8000/docs`로 접속
- 모든 API 엔드포인트를 시각적으로 확인 가능
- 직접 API 테스트 실행 가능

#### 터미널/명령행 인터페이스
- cURL 또는 HTTP 클라이언트 도구 사용
- API 호출을 통한 모든 기능 제어

---

## 2. 잡사이트 URL 등록 방법

### 2.1 크롤링 실행하기

#### 방법 1: 특정 URL로 크롤링
```bash
curl -X POST "http://localhost:8000/api/jobs/crawl" \
-H "Content-Type: application/json" \
-d '{"url": "https://www.saramin.co.kr/zf_user/search/recruit?searchword=개발자"}'
```

#### 방법 2: 기본 크롤링 실행
```bash
curl -X POST "http://localhost:8000/scrape/"
```

### 2.2 지원되는 URL 형식

#### 사람인 검색 URL 예시
- **개발자 검색**: `https://www.saramin.co.kr/zf_user/search/recruit?searchword=개발자`
- **프로그래머 검색**: `https://www.saramin.co.kr/zf_user/search/recruit?searchword=프로그래머`
- **백엔드 검색**: `https://www.saramin.co.kr/zf_user/search/recruit?searchword=백엔드`
- **프론트엔드 검색**: `https://www.saramin.co.kr/zf_user/search/recruit?searchword=프론트엔드`

#### URL 파라미터 설명
| 파라미터 | 설명 | 예시 |
|---------|------|------|
| `searchword` | 검색 키워드 | 개발자, 프로그래머, 백엔드 등 |
| `cat_dept` | 직무 카테고리 | IT·인터넷, 경영·사무 등 |
| `loc_mcd` | 지역 코드 | 서울, 부산, 경기 등 |

### 2.3 크롤링 응답 확인
성공적인 크롤링 요청 시 다음과 같은 응답을 받습니다:
```json
{
  "message": "크롤링이 시작되었습니다. URL: https://www.saramin.co.kr/...",
  "status": "started"
}
```

---

## 3. 크롤링 결과 확인

### 3.1 전체 채용공고 목록 조회
```bash
curl "http://localhost:8000/api/jobs?skip=0&limit=100"
```

### 3.2 특정 채용공고 상세 조회
```bash
curl "http://localhost:8000/api/jobs/1"
```

### 3.3 수집되는 데이터 필드
각 채용공고에는 다음 정보가 포함됩니다:

| 필드명 | 설명 | 예시 |
|-------|------|------|
| `id` | 고유 식별자 | 1, 2, 3... |
| `company_name` | 회사명 | "(주)카카오" |
| `job_title` | 채용 제목 | "백엔드 개발자 모집" |
| `start_date` | 수집일 | "2024-01-15" |
| `end_date` | 마감일 | "상시모집" 또는 "2024-02-15" |
| `applicant_count` | 지원자 수 | 25 |
| `requirements` | 자격요건 | "Java 3년 이상 경험" |
| `preferred_qualifications` | 우대사항 | "Spring Framework 경험" |
| `location` | 근무지역 | "서울 강남구" |
| `source_url` | 원본 URL | "https://www.saramin.co.kr/..." |
| `created_at` | 생성일시 | "2024-01-15T10:30:00" |

---

## 4. 데이터 필터링 및 검색

### 4.1 페이징 처리
```bash
# 처음 10개 가져오기
curl "http://localhost:8000/api/jobs?skip=0&limit=10"

# 11번째부터 20개 가져오기
curl "http://localhost:8000/api/jobs?skip=10&limit=20"
```

### 4.2 회사별 검색 (확장 기능)
시스템에는 `get_job_postings_by_company` 함수가 준비되어 있어, 향후 회사별 검색 API가 추가될 예정입니다.

### 4.3 키워드 검색 (확장 기능)
`search_job_postings` 함수를 통해 다음 필드에서 키워드 검색이 가능합니다:
- 채용 제목 (`job_title`)
- 자격요건 (`requirements`)
- 우대사항 (`preferred_qualifications`)

---

## 5. 지원 이력 관리 팁

### 5.1 효과적인 데이터 활용
1. **정기적인 크롤링**: 매일 또는 주기적으로 크롤링을 실행하여 최신 채용공고 수집
2. **관심 공고 표시**: API를 통해 관심있는 공고의 ID를 별도로 관리
3. **지원 현황 추적**: 외부 도구와 연계하여 지원 현황 관리

### 5.2 데이터 관리 권장사항
```bash
# 1. 매일 새로운 공고 수집
curl -X POST "http://localhost:8000/scrape/"

# 2. 수집된 공고 확인
curl "http://localhost:8000/api/jobs?limit=50"

# 3. 불필요한 공고 삭제
curl -X DELETE "http://localhost:8000/api/jobs/123"
```

### 5.3 백업 및 데이터 관리
- 데이터베이스 파일: `job_tracker.db` (SQLite)
- 정기적인 백업 권장
- 데이터 누적에 따른 성능 고려

---

## 6. 자주 묻는 질문 (FAQ)

### Q1. 크롤링이 시작되지 않아요.
**A**: 다음을 확인해보세요:
- 서버가 실행 중인지 확인 (`http://localhost:8000` 접속 테스트)
- URL 형식이 올바른지 확인
- 네트워크 연결 상태 확인

### Q2. 수집되는 공고 수가 적어요.
**A**: 현재 설정상 다음과 같은 제한이 있습니다:
- 검색 결과당 최대 10개 공고 수집
- 요청 간격 2초 (서버 부하 방지)
- 이는 `saramin_spider.py:36`에서 수정 가능합니다

### Q3. 특정 회사나 키워드로 검색하고 싶어요.
**A**: 현재는 URL 파라미터를 통해서만 가능합니다:
```
https://www.saramin.co.kr/zf_user/search/recruit?searchword=원하는키워드
```

### Q4. 데이터베이스가 너무 커져요.
**A**: 다음 방법으로 관리할 수 있습니다:
```bash
# 특정 공고 삭제
curl -X DELETE "http://localhost:8000/api/jobs/{job_id}"

# 또는 데이터베이스 파일 직접 관리
```

### Q5. 크롤링 속도를 높이고 싶어요.
**A**: `scrapy_project/spiders/saramin_spider.py`에서 설정 변경:
```python
custom_settings = {
    'DOWNLOAD_DELAY': 1,  # 2에서 1로 변경 (주의: 너무 빠르면 차단될 수 있음)
    'CONCURRENT_REQUESTS': 2,  # 동시 요청 수 증가
}
```

### Q6. 다른 채용 사이트도 지원되나요?
**A**: 현재는 사람인만 지원됩니다. 다른 사이트 추가는 개발 확장이 필요합니다.

---

## 7. 지원되는 사이트 목록

### 7.1 현재 지원 사이트

#### 사람인 (Saramin)
- **도메인**: `saramin.co.kr`
- **지원 페이지 유형**:
  - 검색 결과 페이지
  - 개별 채용공고 상세 페이지
- **수집 가능 정보**:
  - 회사명, 채용 제목
  - 모집 기간 (시작일/마감일)
  - 지원자 수
  - 자격요건 및 우대사항
  - 근무지역
  - 원본 URL

### 7.2 크롤링 윤리 및 제한사항

#### 현재 적용된 제한
```python
custom_settings = {
    'DOWNLOAD_DELAY': 2,                    # 요청 간 2초 대기
    'CONCURRENT_REQUESTS': 1,               # 전체 동시 요청 1개
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,    # 도메인당 동시 요청 1개
}
```

#### 준수 사항
- **robots.txt 확인**: 웹사이트 정책 준수
- **적절한 지연시간**: 서버 부하 방지
- **개인정보 보호**: 민감한 정보 수집 금지
- **교육/연구 목적**: 상업적 이용 시 별도 확인 필요

### 7.3 향후 확장 계획
현재 아키텍처는 다른 사이트 추가가 용이하도록 설계되어 있습니다:
- 새로운 스파이더 클래스 추가
- 사이트별 데이터 처리 파이프라인 구성
- 통합 API 인터페이스 유지

---

## 🔧 문제 해결

### 로그 확인
시스템 실행 시 콘솔에서 로그를 확인할 수 있습니다:
```bash
python main.py
```

### 데이터베이스 직접 확인
```bash
sqlite3 job_tracker.db
.tables
SELECT * FROM job_postings LIMIT 10;
```

### 서비스 재시작
문제 발생 시 서버를 재시작하세요:
1. `Ctrl+C`로 서버 중지
2. `python main.py`로 재시작

---

## ⚠️ 중요 알림

### 법적 고지
- 본 도구는 **교육 및 연구 목적**으로만 사용하세요
- 웹사이트 이용약관과 저작권법을 준수하세요
- 과도한 크롤링은 피해주세요

### 보안 권장사항
- 프로덕션 환경에서는 인증/권한 시스템 구현
- 정기적인 데이터 백업
- 보안 업데이트 적용

---

*마지막 업데이트: 2024년 1월*

문의사항이 있으시면 프로젝트 저장소의 이슈 트래커를 활용해 주세요.
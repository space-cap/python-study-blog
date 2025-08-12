# Job Tracker 설치 및 설정 가이드

사람인(Saramin) 채용사이트 크롤링 및 채용정보 추적 API 서비스의 상세한 설치 및 설정 가이드입니다.

## 📋 목차
- [시스템 요구사항](#시스템-요구사항)
- [Python 환경 설정](#python-환경-설정)
- [가상환경 생성 및 활성화](#가상환경-생성-및-활성화)
- [의존성 설치](#의존성-설치)
- [데이터베이스 초기화](#데이터베이스-초기화)
- [환경변수 설정](#환경변수-설정)
- [개발 서버 실행](#개발-서버-실행)
- [트러블슈팅](#트러블슈팅)

## 🖥️ 시스템 요구사항

### 최소 사양
- **운영체제**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 이상 (3.9+ 권장)
- **메모리**: 최소 4GB RAM (8GB 권장)
- **디스크**: 최소 1GB 여유 공간
- **네트워크**: 인터넷 연결 (크롤링 작업 시 필요)

### 권장 사양
- **Python**: 3.11+
- **메모리**: 8GB+ RAM
- **디스크**: SSD 권장
- **기타**: Visual Studio Code 또는 PyCharm (개발 편의성)

## 🐍 Python 환경 설정

### 1. Python 설치 확인

```bash
# Python 버전 확인
python --version
# 또는
python3 --version
```

### 2. Python 설치 (버전이 없거나 낮은 경우)

#### Windows
1. [Python 공식 웹사이트](https://python.org/downloads/)에서 최신 버전 다운로드
2. 설치 시 "Add Python to PATH" 옵션 체크
3. 설치 완료 후 터미널 재시작

#### macOS
```bash
# Homebrew 사용
brew install python@3.11

# 또는 공식 설치 프로그램 사용
# https://python.org/downloads/에서 다운로드
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### CentOS/RHEL
```bash
sudo yum install python3 python3-pip
# 또는 dnf (최신 버전)
sudo dnf install python3 python3-pip
```

### 3. pip 업그레이드
```bash
python -m pip install --upgrade pip
```

## 📦 가상환경 생성 및 활성화

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd job-tracker
```

### 2. 가상환경 생성
```bash
# Python 3.8+에서 권장되는 방법
python -m venv .venv

# 또는 특정 Python 버전 사용 (Linux/Mac)
python3.11 -m venv .venv
```

### 3. 가상환경 활성화

#### Windows (Command Prompt)
```cmd
.venv\Scripts\activate.bat
```

#### Windows (PowerShell)
```powershell
.venv\Scripts\Activate.ps1
```

**PowerShell 실행 정책 오류 해결:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Linux/macOS
```bash
source .venv/bin/activate
```

### 4. 가상환경 활성화 확인
활성화가 성공하면 터미널 프롬프트 앞에 `(.venv)`가 표시됩니다:
```bash
(.venv) user@computer:~/job-tracker$
```

## 🔧 의존성 설치

### 1. 기본 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 개발 의존성 별도 설치 (선택사항)
```bash
# 개발 도구만 설치하려는 경우
pip install pytest pytest-asyncio black isort flake8
```

### 3. 설치 확인
```bash
# 설치된 패키지 목록 확인
pip list

# 주요 패키지 버전 확인
pip show fastapi uvicorn scrapy sqlalchemy
```

### 주요 의존성 설명

#### 웹 프레임워크
- **FastAPI** (0.104.1): 고성능 웹 API 프레임워크
- **Uvicorn** (0.24.0): ASGI 서버
- **Pydantic** (2.5.0): 데이터 검증 및 설정 관리

#### 데이터베이스
- **SQLAlchemy** (2.0.23): ORM 및 데이터베이스 관리
- **Alembic** (1.13.1): 데이터베이스 마이그레이션

#### 웹 크롤링
- **Scrapy** (2.11.0): 웹 크롤링 프레임워크
- **scrapy-user-agents**: 다양한 User-Agent 사용
- **scrapy-rotating-proxies**: 프록시 로테이션

## 🗄️ 데이터베이스 초기화

### 1. 데이터베이스 자동 생성
프로젝트는 SQLite를 사용하며, 첫 실행 시 자동으로 데이터베이스가 생성됩니다.

### 2. 데이터베이스 파일 위치
```
job-tracker/
└── job_tracker.db  # SQLite 데이터베이스 파일
```

### 3. 테이블 구조 확인 (선택사항)
```bash
# SQLite CLI를 사용한 테이블 확인
sqlite3 job_tracker.db
.tables
.schema job_postings
.exit
```

### 4. 데이터베이스 초기화 (필요시)
데이터베이스를 초기화하려면:
```bash
# 데이터베이스 파일 삭제 후 재생성
rm job_tracker.db  # Linux/Mac
del job_tracker.db  # Windows

# 애플리케이션 재실행 시 자동 생성
python main.py
```

## ⚙️ 환경변수 설정

### 1. 환경변수 파일 생성
프로젝트 루트에 `.env` 파일을 생성합니다:

```bash
# .env 파일 생성
touch .env  # Linux/Mac
type nul > .env  # Windows
```

### 2. 환경변수 설정 예시
`.env` 파일에 다음 내용을 추가:

```bash
# 데이터베이스 설정
DATABASE_URL=sqlite:///./job_tracker.db

# API 서버 설정
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true

# Scrapy 설정
SCRAPY_LOG_LEVEL=INFO
SCRAPY_USER_AGENT=job-tracker (+http://www.yourdomain.com)

# 크롤링 제한 설정 (윤리적 크롤링)
SARAMIN_DELAY=1
CONCURRENT_REQUESTS=1
CONCURRENT_REQUESTS_PER_DOMAIN=1
```

### 3. 환경변수 설명

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `DATABASE_URL` | `sqlite:///./job_tracker.db` | 데이터베이스 연결 URL |
| `API_HOST` | `0.0.0.0` | API 서버 호스트 |
| `API_PORT` | `8000` | API 서버 포트 |
| `API_DEBUG` | `true` | 디버그 모드 활성화 |
| `SCRAPY_LOG_LEVEL` | `INFO` | Scrapy 로그 레벨 |
| `SCRAPY_USER_AGENT` | `job-tracker (+http://www.yourdomain.com)` | 크롤링 시 사용할 User-Agent |
| `SARAMIN_DELAY` | `1` | 요청 간 딜레이 (초) |
| `CONCURRENT_REQUESTS` | `1` | 동시 요청 수 |
| `CONCURRENT_REQUESTS_PER_DOMAIN` | `1` | 도메인당 동시 요청 수 |

### 4. 보안 주의사항
- `.env` 파일은 절대 Git에 커밋하지 마세요
- `.gitignore`에 `.env`가 포함되어 있는지 확인하세요

## 🚀 개발 서버 실행

### 1. 기본 실행
```bash
# 가상환경이 활성화된 상태에서
python main.py
```

### 2. Uvicorn을 직접 사용한 실행
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 프로덕션 모드 실행
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. 서비스 접속 확인
브라우저에서 다음 URL들을 확인:

- **메인 페이지**: http://localhost:8000
- **API 문서 (Swagger)**: http://localhost:8000/docs
- **ReDoc 문서**: http://localhost:8000/redoc

### 5. API 테스트
```bash
# 루트 엔드포인트 테스트
curl http://localhost:8000/

# 채용공고 목록 조회
curl http://localhost:8000/api/jobs

# 크롤링 실행 테스트
curl -X POST http://localhost:8000/api/jobs/crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.saramin.co.kr/zf_user/search/recruit?searchword=개발자"}'
```

## 🔧 트러블슈팅

### Python 관련 문제

#### 문제: `python` 명령어를 찾을 수 없음
```bash
# 해결방법 1: python3 사용
python3 --version
python3 -m venv .venv

# 해결방법 2: PATH 환경변수 확인 (Windows)
# 시스템 환경변수에 Python 경로 추가

# 해결방법 3: 별칭 생성 (Linux/Mac)
alias python=python3
```

#### 문제: `pip` 명령어를 찾을 수 없음
```bash
# 해결방법 1: python -m pip 사용
python -m pip install --upgrade pip

# 해결방법 2: pip3 사용
pip3 install -r requirements.txt

# 해결방법 3: pip 재설치 (Ubuntu)
sudo apt install python3-pip
```

### 가상환경 관련 문제

#### 문제: PowerShell에서 가상환경 활성화 실패
```powershell
# ExecutionPolicy 변경
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 또는 우회 실행
powershell -ExecutionPolicy Bypass -File .venv\Scripts\Activate.ps1
```

#### 문제: 가상환경이 생성되지 않음
```bash
# venv 모듈 설치 (Ubuntu/Debian)
sudo apt install python3-venv

# 또는 virtualenv 사용
pip install virtualenv
virtualenv .venv
```

### 의존성 설치 문제

#### 문제: `requirements.txt` 설치 실패
```bash
# pip 업그레이드 후 재시도
python -m pip install --upgrade pip
pip install -r requirements.txt

# 개별 패키지 설치 시도
pip install fastapi uvicorn sqlalchemy

# 캐시 클리어 후 재시도
pip install --no-cache-dir -r requirements.txt
```

#### 문제: Scrapy 설치 실패 (Windows)
```bash
# Microsoft Visual C++ 14.0 설치
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

# 또는 wheel 파일 사용
pip install --only-binary=all scrapy
```

#### 문제: 특정 패키지 설치 실패
```bash
# 시스템 의존성 설치 (Ubuntu)
sudo apt install build-essential python3-dev libffi-dev libssl-dev

# macOS에서 Xcode Command Line Tools 설치
xcode-select --install
```

### 데이터베이스 관련 문제

#### 문제: SQLite 데이터베이스 권한 오류
```bash
# 파일 권한 확인 및 수정
ls -la job_tracker.db
chmod 644 job_tracker.db

# 디렉토리 권한 확인
chmod 755 .
```

#### 문제: 데이터베이스 테이블이 생성되지 않음
```bash
# 데이터베이스 파일 삭제 후 재생성
rm job_tracker.db
python main.py

# 또는 Python 스크립트로 강제 생성
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

### 서버 실행 문제

#### 문제: 포트 8000이 이미 사용 중
```bash
# 다른 포트 사용
uvicorn main:app --host 0.0.0.0 --port 8001

# 또는 환경변수로 포트 변경
export API_PORT=8001  # Linux/Mac
set API_PORT=8001     # Windows CMD

# 사용 중인 프로세스 확인 및 종료
# Linux/Mac
sudo lsof -i :8000
sudo kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### 문제: 모듈을 찾을 수 없음 (`ModuleNotFoundError`)
```bash
# PYTHONPATH 설정
export PYTHONPATH=$PYTHONPATH:$(pwd)  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%CD%      # Windows

# 또는 프로젝트 루트에서 실행
cd /path/to/job-tracker
python main.py
```

### 크롤링 관련 문제

#### 문제: 크롤링이 동작하지 않음
```bash
# Scrapy 설정 확인
scrapy list

# 스파이더 직접 실행 테스트
cd scrapy_project
scrapy crawl saramin

# 로그 레벨을 DEBUG로 변경하여 상세 정보 확인
export SCRAPY_LOG_LEVEL=DEBUG
```

#### 문제: 네트워크 연결 오류
```bash
# DNS 설정 확인
nslookup www.saramin.co.kr

# 프록시 설정 확인
echo $HTTP_PROXY $HTTPS_PROXY

# User-Agent 변경 시도
# config/settings.py에서 SCRAPY_USER_AGENT 수정
```

### 성능 관련 문제

#### 문제: 메모리 사용량이 높음
```python
# config/settings.py에서 동시 요청 수 조정
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
SARAMIN_DELAY = 2  # 딜레이 증가
```

#### 문제: 응답 속도가 느림
```python
# 데이터베이스 인덱스 추가 (필요시)
# app/models.py에서 인덱스 설정

# 또는 메모리 기반 SQLite 사용 (개발 환경)
DATABASE_URL = "sqlite:///:memory:"
```

## 🔍 로그 및 디버깅

### 1. 로그 파일 위치
```bash
# FastAPI 로그는 콘솔에 출력
# Scrapy 로그는 기본적으로 콘솔 출력

# 로그를 파일로 저장하려면:
python main.py > app.log 2>&1

# 또는 nohup 사용 (백그라운드 실행)
nohup python main.py > app.log 2>&1 &
```

### 2. 디버그 모드 활성화
```bash
# .env 파일에서
API_DEBUG=true
SCRAPY_LOG_LEVEL=DEBUG
```

### 3. 상세 오류 정보 확인
```bash
# Python 스택 트레이스 출력
python -u main.py

# 또는 verbose 모드
python main.py --log-level debug
```

## 🚀 추가 설정 (선택사항)

### 1. 개발 도구 설정
```bash
# 코드 포맷팅
black .
isort .

# 코드 린팅
flake8 .

# 타입 체크 (mypy 설치 필요)
pip install mypy
mypy .
```

### 2. 테스트 실행
```bash
# 전체 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/test_api.py

# 커버리지 포함 테스트
pip install pytest-cov
pytest --cov=app tests/
```

### 3. Docker 사용 (선택사항)
```dockerfile
# Dockerfile 예시 (프로젝트에 추가 필요)
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

## 📞 지원 및 문의

설치 과정에서 문제가 발생하면:

1. **GitHub Issues**: 프로젝트 저장소의 Issues 탭에서 문의
2. **로그 확인**: 위의 로그 및 디버깅 섹션 참고
3. **환경 정보 제공**: 
   - 운영체제 및 버전
   - Python 버전
   - 오류 메시지 전문
   - 실행한 명령어

## 📚 다음 단계

설치가 완료되었다면:

1. **API 문서 확인**: http://localhost:8000/docs
2. **기본 API 테스트**: [API.md](./API.md) 참고
3. **크롤링 윤리 준수**: README.md의 주의사항 섹션 확인
4. **커스터마이징**: config/settings.py에서 설정 조정

---

**🎉 축하합니다!** Job Tracker가 성공적으로 설치되었습니다. 이제 사람인 채용공고 크롤링 서비스를 사용할 수 있습니다.
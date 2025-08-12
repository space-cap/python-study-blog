# 제3자 라이브러리 라이선스 정보

본 문서는 Job Tracker 프로젝트에서 사용하는 제3자 라이브러리들의 라이선스 정보를 포함합니다.

**최종 업데이트**: 2024년  
**프로젝트 버전**: 현재 버전

## 📋 주요 의존성 라이브러리

### 🚀 웹 프레임워크

#### FastAPI (0.104.1)
- **라이선스**: MIT License
- **저작권**: Copyright (c) 2018 Sebastián Ramírez
- **용도**: 웹 API 프레임워크
- **라이선스 상세**: https://github.com/tiangolo/fastapi/blob/master/LICENSE

#### Uvicorn (0.24.0)
- **라이선스**: BSD-3-Clause License
- **저작권**: Copyright (c) 2017-present, Tom Christie
- **용도**: ASGI 서버
- **라이선스 상세**: https://github.com/encode/uvicorn/blob/master/LICENSE.md

### 🔍 웹 크롤링

#### Scrapy (2.11.0)
- **라이선스**: BSD-3-Clause License
- **저작권**: Copyright (c) Scrapy developers
- **용도**: 웹 크롤링 프레임워크
- **라이선스 상세**: https://github.com/scrapy/scrapy/blob/master/LICENSE

#### scrapy-user-agents (0.1.1)
- **라이선스**: MIT License
- **저작권**: Copyright (c) 2019 9dogs
- **용도**: 다양한 User-Agent 사용
- **라이선스 상세**: https://github.com/9dogs/scrapy-user-agents/blob/master/LICENSE

#### scrapy-rotating-proxies (0.6.2)
- **라이선스**: MIT License
- **저작권**: Copyright (c) 2015 ScrapingHub
- **용도**: 프록시 로테이션
- **라이선스 상세**: https://github.com/TeamHG-Memex/scrapy-rotating-proxies/blob/master/LICENSE

### 🗄️ 데이터베이스

#### SQLAlchemy (2.0.23)
- **라이선스**: MIT License
- **저작권**: Copyright 2006-2023 the SQLAlchemy authors and contributors
- **용도**: ORM 및 데이터베이스 관리
- **라이선스 상세**: https://github.com/sqlalchemy/sqlalchemy/blob/main/LICENSE

#### Alembic (1.13.1)
- **라이선스**: MIT License
- **저작권**: Copyright (C) 2009-2023 by Michael Bayer
- **용도**: 데이터베이스 마이그레이션
- **라이선스 상세**: https://github.com/sqlalchemy/alembic/blob/main/LICENSE

### 📊 데이터 검증

#### Pydantic (2.5.0)
- **라이선스**: MIT License
- **저작권**: Copyright (c) 2017 to present Samuel Colvin and other contributors
- **용도**: 데이터 검증 및 설정 관리
- **라이선스 상세**: https://github.com/pydantic/pydantic/blob/main/LICENSE

#### pydantic-settings (2.1.0)
- **라이선스**: MIT License
- **저작권**: Copyright (c) 2021 to present Samuel Colvin and other contributors
- **용도**: 설정 관리
- **라이선스 상세**: https://github.com/pydantic/pydantic-settings/blob/main/LICENSE

### 🛠️ 유틸리티

#### Requests (2.31.0)
- **라이선스**: Apache License 2.0
- **저작권**: Copyright 2019 Kenneth Reitz
- **용도**: HTTP 클라이언트 라이브러리
- **라이선스 상세**: https://github.com/psf/requests/blob/main/LICENSE

#### python-multipart (0.0.6)
- **라이선스**: Apache License 2.0
- **저작권**: Copyright 2021 Andrew Dunham
- **용도**: 멀티파트 폼 데이터 처리
- **라이선스 상세**: https://github.com/andrew-d/python-multipart/blob/master/LICENSE.txt

#### python-dotenv (1.0.0)
- **라이선스**: BSD-3-Clause License
- **저작권**: Copyright (c) 2014, Saurabh Kumar
- **용도**: 환경변수 관리
- **라이선스 상세**: https://github.com/theskumar/python-dotenv/blob/main/LICENSE

### 🧪 개발 및 테스트

#### pytest (7.4.3)
- **라이선스**: MIT License
- **저작권**: Copyright (c) 2004 Holger Krekel and others
- **용도**: 테스트 프레임워크
- **라이선스 상세**: https://github.com/pytest-dev/pytest/blob/main/LICENSE

#### pytest-asyncio (0.21.1)
- **라이선스**: Apache License 2.0
- **저작권**: Copyright 2019 pytest-asyncio contributors
- **용도**: 비동기 테스트 지원
- **라이선스 상세**: https://github.com/pytest-dev/pytest-asyncio/blob/main/LICENSE

#### Black (23.11.0)
- **라이선스**: MIT License
- **저작권**: Copyright (c) 2018 Łukasz Langa
- **용도**: 코드 포매터
- **라이선스 상세**: https://github.com/psf/black/blob/main/LICENSE

#### isort (5.12.0)
- **라이선스**: MIT License
- **저작권**: Copyright (c) 2013 Timothy Edmund Crosley
- **용도**: import 문 정렬
- **라이선스 상세**: https://github.com/PyCQA/isort/blob/main/LICENSE

#### flake8 (6.1.0)
- **라이선스**: MIT License
- **저작권**: Copyright (c) 2011-2013 Tarek Ziadé, 2013-2016 Ian Cordasco
- **용도**: 코드 린팅
- **라이선스 상세**: https://github.com/PyCQA/flake8/blob/main/LICENSE

## 📄 라이선스 요약

### MIT License 라이브러리
다음 라이브러리들은 MIT 라이선스를 사용합니다:
- FastAPI, Pydantic, pydantic-settings
- Scrapy, scrapy-user-agents, scrapy-rotating-proxies
- SQLAlchemy, Alembic
- pytest, Black, isort, flake8
- python-dotenv

**MIT 라이선스 주요 조건:**
- ✅ 상업적 사용 허용
- ✅ 수정 및 배포 허용
- ✅ 사적 사용 허용
- ✅ 특허 사용 허용
- ⚠️ 라이선스 및 저작권 고지 필요

### Apache License 2.0 라이브러리
다음 라이브러리들은 Apache License 2.0을 사용합니다:
- Requests, python-multipart
- pytest-asyncio

**Apache License 2.0 주요 조건:**
- ✅ 상업적 사용 허용
- ✅ 수정 및 배포 허용
- ✅ 특허 사용 허용
- ⚠️ 라이선스 및 저작권 고지 필요
- ⚠️ 변경사항 명시 필요

### BSD-3-Clause License 라이브러리
다음 라이브러리들은 BSD-3-Clause 라이선스를 사용합니다:
- Uvicorn, python-dotenv

**BSD-3-Clause 라이선스 주요 조건:**
- ✅ 상업적 사용 허용
- ✅ 수정 및 배포 허용
- ✅ 사적 사용 허용
- ⚠️ 라이선스 및 저작권 고지 필요
- ❌ 저작권자 이름을 광고에 사용 금지

## ⚠️ 중요 고지사항

### 라이선스 준수 의무
본 프로젝트를 사용, 수정, 배포할 때는 다음 사항을 준수해야 합니다:

1. **저작권 고지**: 모든 제3자 라이브러리의 저작권 정보 유지
2. **라이선스 포함**: 해당 라이브러리의 라이선스 텍스트 포함
3. **변경사항 표시**: 원본에서 변경된 사항 명시 (Apache 라이선스의 경우)
4. **면책조항 유지**: 라이선스에 포함된 면책조항 유지

### 라이선스 충돌 방지
- 모든 사용된 라이브러리는 MIT 라이선스와 호환됩니다
- 상업적 사용 시에도 제약이 없습니다
- 다만, 각 라이브러리의 라이선스 조건은 반드시 준수해야 합니다

### 업데이트 및 관리
- 의존성 업데이트 시 라이선스 변경사항 확인 필요
- 새로운 라이브러리 추가 시 라이선스 호환성 검토 필요
- 정기적인 라이선스 정보 업데이트 권장

## 📞 문의사항

라이선스 관련 문의사항이 있으시면:
- 프로젝트 이슈 트래커를 통해 문의
- 각 라이브러리의 공식 문서 확인
- 필요시 법률 전문가와 상담

---

**면책조항**: 본 문서는 정보 제공 목적으로 작성되었으며, 법적 조언을 대체하지 않습니다. 상업적 사용이나 법적 문제가 있는 경우 전문가와 상담하시기 바랍니다.
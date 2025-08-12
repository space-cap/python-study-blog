"""테스트 데이터를 직접 데이터베이스에 추가"""

from app.database import get_db
from app.models import JobPosting
from sqlalchemy.orm import sessionmaker
from app.database import engine

Session = sessionmaker(bind=engine)
session = Session()

# 테스트 데이터 생성
test_job = JobPosting(
    company_name="테스트 회사",
    title="백엔드 개발자 채용",
    start_date="2025-08-12",
    end_date="2025-08-30",
    applicant_count=15,
    requirements="Python, FastAPI 경험자 우대",
    preferred_qualifications="Docker, AWS 경험자 우대",
    location="서울 강남구",
    url="https://example.com/job/1"
)

try:
    session.add(test_job)
    session.commit()
    print("테스트 데이터가 성공적으로 추가되었습니다.")
except Exception as e:
    session.rollback()
    print(f"오류 발생: {e}")
finally:
    session.close()
"""SQLAlchemy 데이터베이스 모델 정의.

채용공고 정보를 저장하기 위한 데이터베이스 모델을 정의합니다.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class JobPosting(Base):
    """채용공고 정보를 저장하는 데이터베이스 모델.
    
    사람인에서 크롤링한 채용공고 정보를 저장하고 관리하기 위한 모델입니다.
    
    Attributes:
        id (int): 기본 키, 자동 증가
        company_name (str): 회사명 (최대 255자, 인덱스 사용)
        title (str): 채용공고 제목 (최대 500자)
        start_date (str): 공고 시작일 또는 발견일 (최대 50자)
        end_date (str): 공고 마감일 (최대 50자)
        applicant_count (int): 지원자 수 (기본값 0)
        requirements (str): 자격요건 (긴 텍스트)
        preferred_qualifications (str): 우대사항 (긴 텍스트)
        location (str): 근무지역 (최대 255자)
        url (str): 원본 채용공고 URL (긴 텍스트)
        salary (str): 급여 정보 (최대 255자)
        employment_type (str): 고용 형태 (최대 100자)
        experience_level (str): 경력 수준 (최대 100자)
        education_level (str): 학력 요건 (최대 100자)
        created_at (datetime): 레코드 생성 시간 (자동 설정)
        updated_at (datetime): 레코드 수정 시간
    """
    __tablename__ = "job_postings"

    # 기본 키 및 식별자
    id = Column(Integer, primary_key=True, index=True)
    
    # 회사 및 채용 기본 정보
    company_name = Column(String(255), nullable=False, index=True)  # 검색 효율성을 위한 인덱스
    title = Column(String(500), nullable=False)
    
    # 일정 정보
    start_date = Column(String(50))  # 공고 시작일 또는 발견일
    end_date = Column(String(50))    # 공고 마감일
    
    # 지원 정보
    applicant_count = Column(Integer, default=0)
    
    # 자격 요건 및 우대사항
    requirements = Column(Text)  # 긴 텍스트를 위해 Text 타입 사용
    preferred_qualifications = Column(Text)
    
    # 위치 및 URL 정보
    location = Column(String(255))
    url = Column(Text)  # URL은 길 수 있으므로 Text 타입 사용
    
    # 추가 채용 정보
    salary = Column(String(255))
    employment_type = Column(String(100))   # 정규직, 계약직, 인턴 등
    experience_level = Column(String(100))  # 신입, 경력, 무관 등
    education_level = Column(String(100))   # 학력 요건
    
    # 메타데이터 (생성/수정 시간)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 레코드 생성 시 자동 설정
    updated_at = Column(DateTime(timezone=True))  # 수동으로 업데이트 필요
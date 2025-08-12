from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    start_date = Column(String(50))
    end_date = Column(String(50))
    applicant_count = Column(Integer, default=0)
    requirements = Column(Text)
    preferred_qualifications = Column(Text)
    location = Column(String(255))
    url = Column(Text)
    salary = Column(String(255))
    employment_type = Column(String(100))
    experience_level = Column(String(100))
    education_level = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))
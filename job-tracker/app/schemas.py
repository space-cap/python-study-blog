from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class JobPostingBase(BaseModel):
    company_name: str
    job_title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    applicant_count: int = 0
    requirements: Optional[str] = None
    preferred_qualifications: Optional[str] = None
    location: Optional[str] = None
    source_url: Optional[str] = None

class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CrawlRequest(BaseModel):
    url: str
    
class CrawlResponse(BaseModel):
    message: str
    status: str
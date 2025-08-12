from sqlalchemy.orm import Session
from app import models, schemas

def get_job_postings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.JobPosting).offset(skip).limit(limit).all()

def get_job_posting(db: Session, job_id: int):
    return db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()

def create_job_posting(db: Session, job: schemas.JobPostingCreate):
    db_job = models.JobPosting(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job_postings_by_company(db: Session, company_name: str):
    return db.query(models.JobPosting).filter(models.JobPosting.company_name == company_name).all()

def search_job_postings(db: Session, keyword: str):
    return db.query(models.JobPosting).filter(
        models.JobPosting.job_title.contains(keyword) | 
        models.JobPosting.requirements.contains(keyword) |
        models.JobPosting.preferred_qualifications.contains(keyword)
    ).all()

def delete_job_posting(db: Session, job_id: int):
    db_job = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
    if db_job:
        db.delete(db_job)
        db.commit()
        return True
    return False
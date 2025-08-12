from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import asyncio
import threading
from multiprocessing import Process

from app.database import get_db, engine
from app.models import Base
from app.schemas import JobPosting, JobPostingCreate, CrawlRequest, CrawlResponse
from app.crud import get_job_postings, get_job_posting, create_job_posting, delete_job_posting
from scrapy_project.runner import run_spider

app = FastAPI(
    title="Job Tracker API",
    description="사람인 잡사이트 크롤링 및 채용정보 추적 API",
    version="1.0.0"
)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Job Tracker API에 오신 것을 환영합니다!"}

# 1. POST /api/jobs/crawl - URL 받아서 크롤링 실행
@app.post("/api/jobs/crawl", response_model=CrawlResponse)
async def crawl_jobs(request: CrawlRequest, background_tasks: BackgroundTasks):
    try:
        # 백그라운드에서 크롤링 실행
        def run_crawling():
            try:
                run_spider()
            except Exception as e:
                print(f"크롤링 실행 중 오류: {e}")
        
        # 백그라운드 태스크로 실행
        background_tasks.add_task(run_crawling)
        
        return CrawlResponse(
            message=f"크롤링이 시작되었습니다. URL: {request.url}",
            status="started"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"크롤링 시작 중 오류 발생: {str(e)}")

# 2. GET /api/jobs - 공고 목록 조회
@app.get("/api/jobs", response_model=List[JobPosting])
async def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = get_job_postings(db, skip=skip, limit=limit)
    return jobs

# 3. GET /api/jobs/{job_id} - 상세 조회
@app.get("/api/jobs/{job_id}", response_model=JobPosting)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = get_job_posting(db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="채용공고를 찾을 수 없습니다.")
    return job

# 4. DELETE /api/jobs/{job_id} - 삭제
@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    success = delete_job_posting(db, job_id=job_id)
    if not success:
        raise HTTPException(status_code=404, detail="채용공고를 찾을 수 없습니다.")
    return {"message": "채용공고가 성공적으로 삭제되었습니다."}

# 기존 엔드포인트들 (하위 호환성)
@app.get("/jobs/", response_model=List[JobPosting])
async def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = get_job_postings(db, skip=skip, limit=limit)
    return jobs

@app.post("/jobs/", response_model=JobPosting)
async def create_job(job: JobPostingCreate, db: Session = Depends(get_db)):
    return create_job_posting(db=db, job=job)

@app.post("/scrape/")
async def start_scraping(background_tasks: BackgroundTasks):
    try:
        def run_crawling():
            try:
                run_spider()
            except Exception as e:
                print(f"크롤링 실행 중 오류: {e}")
        
        background_tasks.add_task(run_crawling)
        return {"message": "크롤링이 시작되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"크롤링 실행 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
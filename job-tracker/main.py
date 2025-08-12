"""Job Tracker API 메인 애플리케이션 모듈.

사람인 잡사이트에서 채용정보를 크롤링하고 관리하는 FastAPI 애플리케이션입니다.
주요 기능:
- 채용공고 크롤링 (사람인)
- 채용공고 CRUD 작업
- RESTful API 제공

Example:
    $ python main.py
    또는
    $ uvicorn main:app --host 0.0.0.0 --port 8000
"""

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

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="Job Tracker API",
    description="사람인 잡사이트 크롤링 및 채용정보 추적 API",
    version="1.0.0"
)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    """루트 엔드포인트.
    
    API 서비스 상태를 확인하고 환영 메시지를 반환합니다.
    
    Returns:
        dict: 환영 메시지가 포함된 딕셔너리
    """
    return {"message": "Job Tracker API에 오신 것을 환영합니다!"}

@app.post("/api/jobs/crawl", response_model=CrawlResponse)
async def crawl_jobs(request: CrawlRequest, background_tasks: BackgroundTasks):
    """채용공고 크롤링을 시작합니다.
    
    사람인 웹사이트에서 채용공고를 크롤링하는 작업을 백그라운드에서 시작합니다.
    크롤링은 비동기적으로 실행되며, 즉시 응답을 반환합니다.
    
    Args:
        request (CrawlRequest): 크롤링 요청 정보 (URL 포함)
        background_tasks (BackgroundTasks): FastAPI 백그라운드 태스크 매니저
        
    Returns:
        CrawlResponse: 크롤링 시작 상태 정보
        
    Raises:
        HTTPException: 크롤링 시작 중 오류 발생 시 500 에러
    """
    try:
        def run_crawling():
            """백그라운드에서 실행되는 크롤링 함수.
            
            예외가 발생해도 백그라운드 태스크가 중단되지 않도록
            try-catch로 감싸서 처리합니다.
            """
            try:
                run_spider()
            except Exception as e:
                print(f"크롤링 실행 중 오류: {e}")
        
        # 백그라운드 태스크로 크롤링 실행
        background_tasks.add_task(run_crawling)
        
        return CrawlResponse(
            message=f"크롤링이 시작되었습니다. URL: {request.url}",
            status="started"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"크롤링 시작 중 오류 발생: {str(e)}")

@app.get("/api/jobs", response_model=List[JobPosting])
async def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """저장된 채용공고 목록을 조회합니다.
    
    데이터베이스에서 채용공고 목록을 페이지네이션과 함께 조회합니다.
    
    Args:
        skip (int, optional): 건너뛸 레코드 수. Defaults to 0.
        limit (int, optional): 반환할 최대 레코드 수. Defaults to 100.
        db (Session, optional): 데이터베이스 세션. Depends(get_db)로 자동 주입.
        
    Returns:
        List[JobPosting]: 채용공고 객체들의 리스트
    """
    jobs = get_job_postings(db, skip=skip, limit=limit)
    return jobs

@app.get("/api/jobs/{job_id}", response_model=JobPosting)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """특정 채용공고의 상세 정보를 조회합니다.
    
    채용공고 ID를 통해 해당 공고의 상세 정보를 조회합니다.
    
    Args:
        job_id (int): 조회할 채용공고의 ID
        db (Session, optional): 데이터베이스 세션. Depends(get_db)로 자동 주입.
        
    Returns:
        JobPosting: 채용공고 상세 정보
        
    Raises:
        HTTPException: 해당 ID의 채용공고가 존재하지 않을 경우 404 에러
    """
    job = get_job_posting(db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="채용공고를 찾을 수 없습니다.")
    return job

@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    """특정 채용공고를 삭제합니다.
    
    채용공고 ID를 통해 해당 공고를 데이터베이스에서 삭제합니다.
    
    Args:
        job_id (int): 삭제할 채용공고의 ID
        db (Session, optional): 데이터베이스 세션. Depends(get_db)로 자동 주입.
        
    Returns:
        dict: 삭제 성공 메시지
        
    Raises:
        HTTPException: 해당 ID의 채용공고가 존재하지 않을 경우 404 에러
    """
    success = delete_job_posting(db, job_id=job_id)
    if not success:
        raise HTTPException(status_code=404, detail="채용공고를 찾을 수 없습니다.")
    return {"message": "채용공고가 성공적으로 삭제되었습니다."}

# 하위 호환성을 위한 레거시 엔드포인트들
@app.get("/jobs/", response_model=List[JobPosting])
async def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """채용공고 목록 조회 (레거시 엔드포인트).
    
    하위 호환성을 위해 유지되는 엔드포인트입니다.
    새로운 코드에서는 /api/jobs를 사용하는 것을 권장합니다.
    
    Args:
        skip (int, optional): 건너뛸 레코드 수. Defaults to 0.
        limit (int, optional): 반환할 최대 레코드 수. Defaults to 100.
        db (Session, optional): 데이터베이스 세션. Depends(get_db)로 자동 주입.
        
    Returns:
        List[JobPosting]: 채용공고 객체들의 리스트
    """
    jobs = get_job_postings(db, skip=skip, limit=limit)
    return jobs

@app.post("/jobs/", response_model=JobPosting)
async def create_job(job: JobPostingCreate, db: Session = Depends(get_db)):
    """새로운 채용공고를 생성합니다 (레거시 엔드포인트).
    
    하위 호환성을 위해 유지되는 엔드포인트입니다.
    
    Args:
        job (JobPostingCreate): 생성할 채용공고 정보
        db (Session, optional): 데이터베이스 세션. Depends(get_db)로 자동 주입.
        
    Returns:
        JobPosting: 생성된 채용공고 정보
    """
    return create_job_posting(db=db, job=job)

@app.post("/scrape/")
async def start_scraping(background_tasks: BackgroundTasks):
    """크롤링을 시작합니다 (레거시 엔드포인트).
    
    하위 호환성을 위해 유지되는 엔드포인트입니다.
    새로운 코드에서는 /api/jobs/crawl을 사용하는 것을 권장합니다.
    
    Args:
        background_tasks (BackgroundTasks): FastAPI 백그라운드 태스크 매니저
        
    Returns:
        dict: 크롤링 시작 메시지
        
    Raises:
        HTTPException: 크롤링 시작 중 오류 발생 시 500 에러
    """
    try:
        def run_crawling():
            """백그라운드에서 실행되는 크롤링 함수."""
            try:
                run_spider()
            except Exception as e:
                print(f"크롤링 실행 중 오류: {e}")
        
        background_tasks.add_task(run_crawling)
        return {"message": "크롤링이 시작되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"크롤링 실행 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    # 개발 환경에서 직접 실행 시 uvicorn 서버 시작
    uvicorn.run(app, host="0.0.0.0", port=8000)
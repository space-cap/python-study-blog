#!/usr/bin/env python3
"""크롤링 테스트 스크립트

사람인 웹사이트에서 직접 크롤링을 테스트하고 데이터베이스에 저장하는 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models import JobPosting
from scrapy_project.items import JobPostingItem
from scrapy_project.spiders.saramin_spider import SaraminSpider
from scrapy.http import HtmlResponse
import re

def test_direct_crawling():
    """직접 크롤링 테스트"""
    url = 'https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx=51507890&view_type=search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ko,en;q=0.9',
    }
    
    print("=== 사람인 크롤링 테스트 시작 ===")
    
    try:
        # 1. 웹 페이지 요청
        print(f"1. 페이지 요청: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   응답 코드: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   오류: HTTP {response.status_code}")
            return False
            
        # 2. 스파이더로 정보 추출
        print("2. 정보 추출 중...")
        scrapy_response = HtmlResponse(url=url, body=response.content, encoding='utf-8')
        spider = SaraminSpider()
        
        items = list(spider.parse_job_detail(scrapy_response))
        print(f"   추출된 아이템 수: {len(items)}")
        
        if not items:
            print("   오류: 아이템을 추출하지 못했습니다.")
            return False
            
        # 3. 데이터베이스에 저장
        print("3. 데이터베이스 저장 중...")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        saved_count = 0
        for item in items:
            try:
                job_posting = JobPosting(
                    company_name=item.get('company_name'),
                    title=item.get('job_title'),
                    start_date=item.get('start_date'),
                    end_date=item.get('end_date'),
                    applicant_count=item.get('applicant_count', 0),
                    requirements=item.get('requirements'),
                    preferred_qualifications=item.get('preferred_qualifications'),
                    location=item.get('location'),
                    url=item.get('source_url')
                )
                session.add(job_posting)
                session.commit()
                saved_count += 1
                
                print(f"   저장 완료: {item.get('company_name')} - {item.get('job_title')}")
                
            except Exception as e:
                session.rollback()
                print(f"   저장 오류: {e}")
        
        session.close()
        print(f"   총 {saved_count}개 아이템 저장 완료")
        
        # 4. 저장된 데이터 확인
        print("4. 저장된 데이터 확인...")
        session = Session()
        total_count = session.query(JobPosting).count()
        recent_jobs = session.query(JobPosting).order_by(JobPosting.created_at.desc()).limit(3).all()
        
        print(f"   데이터베이스 총 레코드 수: {total_count}")
        print("   최근 저장된 레코드:")
        for job in recent_jobs:
            print(f"     - {job.company_name}: {job.title} ({job.created_at})")
            
        session.close()
        
        print("=== 크롤링 테스트 성공 ===")
        return True
        
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_direct_crawling()
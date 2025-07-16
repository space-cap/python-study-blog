import os
from typing import Dict, Any
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """설정 정보 관리 클래스"""
    
    # 데이터베이스 설정
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'your_username'),
        'password': os.getenv('DB_PASSWORD', 'your_password'),
        'database': os.getenv('DB_NAME', 'youth_policy_db'),
        'port': int(os.getenv('DB_PORT', 3306))
    }
    
    # API 설정
    API_CONFIG = {
        'base_url': 'https://www.youthcenter.go.kr/go/ythip/getPlcy',
        'api_key': os.getenv('API_KEY', 'testKey'),
        'api_sn': '86',
        'timeout': 30,
        'retry_count': 3,
        'retry_delay': 1
    }
    
    # 로깅 설정
    LOGGING_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'youth_policy_sync.log'
    }
    
    # 페이징 설정
    PAGINATION_CONFIG = {
        'page_size': 100,
        'max_pages': 1000,
        'delay_between_requests': 0.5
    }

# 환경변수 설정 예시 (.env 파일)
"""
DB_HOST=localhost
DB_USER=youth_policy_user
DB_PASSWORD=your_secure_password
DB_NAME=youth_policy_db
DB_PORT=3306
API_KEY=testKey
"""

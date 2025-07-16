import os
from typing import Dict, Any

class OpenSearchConfig:
    """OpenSearch 설정 정보 관리 클래스"""
    
    # OpenSearch 연결 설정
    OPENSEARCH_CONFIG = {
        'host': os.getenv('OPENSEARCH_HOST', 'localhost'),
        'port': int(os.getenv('OPENSEARCH_PORT', 9200)),
        'username': os.getenv('OPENSEARCH_USERNAME'),
        'password': os.getenv('OPENSEARCH_PASSWORD'),
        'use_ssl': os.getenv('OPENSEARCH_USE_SSL', 'false').lower() == 'true',
        'verify_certs': os.getenv('OPENSEARCH_VERIFY_CERTS', 'false').lower() == 'true'
    }
    
    # 인덱스 설정
    INDEX_CONFIG = {
        'name': 'youth_policies',
        'mapping_file': 'opensearch_mapping.json',
        'shards': 1,
        'replicas': 0
    }
    
    # API 설정
    API_CONFIG = {
        'base_url': 'https://www.youthcenter.go.kr/cmnFooter/testbed',
        'api_key': os.getenv('API_KEY', 'testKey'),
        'api_sn': '86',
        'timeout': 30,
        'page_size': 100
    }
    
    # 벌크 인덱싱 설정
    BULK_CONFIG = {
        'batch_size': 100,
        'max_retries': 3,
        'retry_delay': 1
    }
    
    # 로깅 설정
    LOGGING_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'opensearch_sync.log'
    }

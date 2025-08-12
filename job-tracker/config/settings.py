from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "sqlite:///./job_tracker.db"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = True
    
    scrapy_log_level: str = "INFO"
    scrapy_user_agent: str = "job-tracker (+http://www.yourdomain.com)"
    
    saramin_delay: int = 1
    concurrent_requests: int = 1
    concurrent_requests_per_domain: int = 1
    
    class Config:
        env_file = ".env"

settings = Settings()
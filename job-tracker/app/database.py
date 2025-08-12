"""SQLAlchemy 데이터베이스 연결 및 설정 모듈.

데이터베이스 엔진, 세션, Base 클래스 등을 설정하고
FastAPI에서 사용할 데이터베이스 세션 의존성 주입을 제공합니다.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# SQLite 데이터베이스 엔진 생성
# check_same_thread=False: SQLite에서 멀티스레드 사용을 위해 필요
engine = create_engine(
    settings.database_url, 
    connect_args={"check_same_thread": False}
)

# 데이터베이스 세션 팩토리 생성
# autocommit=False: 수동으로 커밋하도록 설정
# autoflush=False: 수동으로 플러시하도록 설정 (성능 최적화)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy ORM 모델들이 상속받을 기본 클래스
Base = declarative_base()

def get_db():
    """데이터베이스 세션 의존성 주입 함수.
    
    FastAPI의 Dependency Injection 시스템과 함께 사용되어
    각 API 요청마다 데이터베이스 세션을 생성하고 자동으로 정리합니다.
    
    Yields:
        Session: SQLAlchemy 데이터베이스 세션 객체
        
    Note:
        try-finally 구문을 사용하여 예외 발생 시에도
        세션이 제대로 닫히도록 보장합니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # 세션 사용 완료 후 자원 정리
        db.close()
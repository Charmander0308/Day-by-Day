from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 사용할 DB 주소 (SQLite는 파일이라서 경로만 적으면 됨)
# 실행하면 프로젝트 폴더에 'daybyday.db'라는 파일 생성
SQLALCHEMY_DATABASE_URL = "sqlite:///./daybyday.db"

# DB 엔진 생성 (커넥션 풀 관리자)
# connect_args={"check_same_thread": False}는 SQLite에서만 필요한 설정
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 데이터베이스 세션 생성기 (JPA의 EntityManager와 비슷)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델(Entity)들이 상속받을 기본 클래스
Base = declarative_base()
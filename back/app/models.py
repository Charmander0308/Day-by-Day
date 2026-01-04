from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class News(Base):
    # 테이블 이름 지정 (@Table(name="news"))
    __tablename__ = "news"

    # 컬럼 정의
    id = Column(Integer, primary_key=True, index=True)  # PK
    title = Column(String, nullable=False)              # 기사 제목
    link = Column(String, unique=True, nullable=False)  # 기사 링크 (중복 방지)
    image_url = Column(String, nullable=True)           # 이미지 링크
    description = Column(Text, nullable=True)                  # 짧은 설명
    
    # 생성 시간 자동 기록 (JPA의 @CreatedDate)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
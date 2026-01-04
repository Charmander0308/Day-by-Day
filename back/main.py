import os
from datetime import datetime
from typing import Optional

import pandas as pd
from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import models, database, crawler, crud

# DB 테이블 생성
# models.py에 정의된 클래스들을 보고, DB에 실제로 테이블을 만듦
# (JPA의 hibernate.ddl-auto = update 와 같은 역할)
models.Base.metadata.create_all(bind=database.engine)

# FastAPI 앱 초기화
app = FastAPI()

# Cors 설정 추가
origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_credentials=True,
    allow_methods=["*"],       
    allow_headers=["*"],       
)

# DB 세션 의존성 주입
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 다운로드 완료 후 파일 삭제를 위한 함수
def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)

# 테스트 API
@app.get("/")
def read_root():
    return {"message": "Hello, Day-by-Day!"}

# 뉴스를 긁어와서 DB에 저장하는 API
@app.post("/news/crawl")
def crawl_news(keyword: str = "에듀테크", db: Session = Depends(get_db)):
    # 크롤러 가동
    news_list = crawler.get_news_data(keyword)
    news_list.reverse()
    
    saved_count = 0
    for news in news_list:
        # DB 저장 (crud.py 호출)
        result = crud.create_news(
            db=db, 
            title=news['title'], 
            link=news['link'],
            image_url=news['image_url'],
            description=news['description']
        )
        if result:
            saved_count += 1
            
    return {
        "message": "크롤링 완료!", 
        "total_found": len(news_list), 
        "newly_saved": saved_count
    }

# DB에 저장된 뉴스를 보여주는 API
@app.get("/news")
def read_news(db: Session = Depends(get_db)):
    return crud.get_all_news(db)

# DB 초기화 API
@app.delete("/news/reset")
def reset_news(db: Session = Depends(get_db)):
    crud.delete_all_news(db)
    return {"message": "초기화 완료"}

# 엑셀 다운로드 API
@app.get("/news/export")
def export_news(limit: Optional[int] = None, background_tasks: BackgroundTasks = BackgroundTasks(), db: Session = Depends(get_db)):
    # DB에서 뉴스 데이터 조회 쿼리 생성
    # 최신순으로 정렬
    query = db.query(models.News).order_by(models.News.id.desc())
    
    # limit가 있으면 개수 제한, 없으면 전체 조회
    if limit:
        news_list = query.limit(limit).all()
    else:
        news_list = query.all()

    if not news_list:
        return {"message": "저장된 뉴스가 없습니다."}
    
    # 엑셀로 만들 데이터 정리
    data = []
    for news in news_list:
        data.append({
            "번호": news.id,
            "제목": news.title,
            "링크": news.link,
            "요약": news.description,  
            "이미지주소": news.image_url,
            "수집일시": news.created_at.strftime("%Y-%m-%d %H:%M:%S") if news.created_at else ""
        })
    
    # 엑셀 파일 생성
    df = pd.DataFrame(data)
    
    # 파일명: news_20260104_221000.xlsx
    count_str = f"_top{limit}" if limit else "_all"
    filename = f"news{count_str}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = f"./{filename}"
    
    # 엑셀로 저장 (index=False는 숫자 빼고 저장)
    df.to_excel(filepath, index=False)

    # 요청 응답 후 파일 삭제 예약(remove_file 함수 실행)
    background_tasks.add_task(remove_file, filepath)
    
    # 사용자가 다운로드할 수 있게 파일 보내주기
    return FileResponse(
        filepath, 
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
        filename=filename
    )
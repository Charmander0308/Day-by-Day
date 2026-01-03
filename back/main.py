from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware 
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

# DB 세션을 빌려주고 반납하는 함수 
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
            img_url=news['image_url'],
            desc=news['desc']
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

# 테스트 API
@app.get("/")
def read_root():
    return {"message": "Hello, Day-by-Day!"}
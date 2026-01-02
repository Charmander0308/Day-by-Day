from sqlalchemy.orm import Session
from . import models

def create_news(db: Session, title: str, link: str):
    # 중복 검사 (이미 저장된 링크인지 확인)
    # SELECT * FROM news WHERE link = ? 와 동일
    existing_news = db.query(models.News).filter(models.News.link == link).first()
    
    if existing_news:
        return None # 이미 있으면 저장 안 함

    # 데이터 생성 (Entity 생성)
    new_news = models.News(title=title, link=link)
    
    # DB에 저장 (persist & commit)
    db.add(new_news)
    db.commit()
    db.refresh(new_news) # 저장된 후의 ID값 등을 갱신
    
    return new_news

def get_all_news(db: Session):
    # SELECT * FROM news ORDER BY id DESC 와 동일
    return db.query(models.News).order_by(models.News.id.desc()).all()

def delete_all_news(db: Session):
    # DELETE FROM news 와 동일
    db.query(models.News).delete()
    db.commit()
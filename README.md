# 📰 Day-by-Day: 교육 뉴스 아카이빙 서비스

## 📖 프로젝트 소개
**Day-by-Day**는 특정 키워드(기본: 에듀테크)와 관련된 최신 뉴스를 크롤링하여 데이터베이스에 영구 저장하고, 웹 인터페이스를 통해 효율적으로 관리/조회할 수 있는 **뉴스 아카이빙 서비스**입니다.

단순한 정보 수집을 넘어, **휘발되는 웹상의 데이터를 정형 데이터(DB)로 자산화**하여 업무 자동화 및 트렌드 분석의 기초를 마련하기 위해 개발되었습니다.

## 🛠 기술 스택 (Tech Stack)

### Backend
* **Language:** Python 3.x
* **Framework:** FastAPI
* **Database:** SQLite (SQLAlchemy ORM)
* **Crawling:** BeautifulSoup4, Requests
* **Architecture:** MVC Pattern (Layered Architecture)

### Frontend
* **Framework:** Vue.js 3 (Composition API)
* **Build Tool:** Vite
* **Styling:** Bootstrap 5
* **HTTP Client:** Axios

## ✨ 주요 기능 (Key Features)
1.  **뉴스 크롤링 & 저장:** '다음(Daum) 뉴스'에서 키워드 기반의 최신 기사 수집 및 중복 방지 저장
2.  **데이터 조회 (Pagination):** 수집된 뉴스를 10개씩 페이지네이션하여 조회
3.  **RESTful API:** 프론트엔드와 백엔드 간의 명확한 데이터 통신 규약 준수
4.  **SPA (Single Page Application):** Vue.js 컴포넌트 기반의 끊김 없는 사용자 경험 제공
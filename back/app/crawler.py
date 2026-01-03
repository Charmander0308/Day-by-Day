import requests
from bs4 import BeautifulSoup

def get_news_data(keyword):
    # 네이버 뉴스 검색 URL (query 부분에 키워드가 들어감)
    # url = f"https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={keyword}"

    # 네이버뉴스의 스마트 블록 UI의 동적 클래스 난독화 때문에 구조가 정형화된 다음으로 변경
    url = f"https://search.daum.net/search?w=news&q={keyword}"

    # 로봇이 아님을 증명하기 위한 헤더
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 뉴스 기사 리스트 가져오기 (CSS 선택자 사용)
    # news_elements = soup.select("a.news_tit")

    # 다음의 선택자로 변경
    news_elements = soup.select("ul.c-list-basic > li")
    if not news_elements:
        news_elements = soup.select("ul.list_news > li")

    results = []
    
    for news in news_elements[:10]:  
        news_tag = news.select_one(".item-title a")
        if not news_tag:
            news_tag = news.select_one(".tit_main")    

        if news_tag:
            title = news_tag.get_text().strip()
            link = news_tag["href"]

            img_tag = news.select_one(".thumb_img, .thumb_g, .wrap_thumb img, .c-item-content img")
            img_url = None
            if img_tag:
                img_url = img_tag.get('data-original-src') or img_tag.get('src')

            desc_tag = news.select_one("p.desc")
            if not desc_tag:
                desc_tag = news.select_one("p.desc")

            desc = desc_tag.get_text().strip() if desc_tag else ""

            news_data = {
                "title": title,
                "link": link,
                "image_url" : img_url,
                "desc" : desc
            }
            results.append(news_data)
            
    return results

# 테스트 실행 코드 (Java의 main 메서드 역할)
if __name__ == "__main__":
    data = get_news_data("에듀테크")

    if not data:
        print("데이터를 가져오지 못했습니다.")
    else:
        for idx, item in enumerate(data, 1):
            print(f"[{idx}] {item['title']}")
            print(f"   링크: {item['link']}")
            print("-" * 50)
import requests, re, time
from bs4 import BeautifulSoup

def get_news_data(keyword: str, limit: int = 10, sort_mode: str = "recency"):
    results = []
    page = 1

    while len(results) < limit:
        url = f"https://search.daum.net/search?w=news&q={keyword}&DA=PGD&spacing=0&p={page}&sort={sort_mode}"

        # 로봇이 아님을 증명하기 위한 헤더
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 뉴스 기사 리스트 가져오기 (CSS 선택자 사용)
            # 다음의 선택자로 변경
            news_elements = soup.select("ul.c-list-basic > li")
            if not news_elements:
                news_elements = soup.select("ul.list_news > li")
            
            if not news_elements:
                break

            for news in news_elements:  
                if len(results) >= limit:
                    break

                news_tag = news.select_one(".item-title a") or news.select_one(".tit_main") or news.select_one("a.tit_main")
                if not news_tag: continue

                if news_tag:
                    title = news_tag.get_text().strip()
                    link = news_tag["href"]

                    img_tag = news.select_one(".thumb_img, .thumb_g, .wrap_thumb img, .c-item-content img")
                    image_url = None
                    if img_tag:
                        image_url = img_tag.get('data-original-src') or img_tag.get('src')

                    for useless in news.select(".screen_out, .blind, .util_view, .layer_util, .box_done"):
                        useless.decompose()

                    desc_selectors = [
                        "p.desc",
                        "div.dsc",
                        ".item-contents",
                        ".f_eb", ".f_nb",
                        ".link_desc",
                        ".wrap_cont p",
                        ".cont_thumb .cont_text p",
                        ".txt_inline",
                        "p.txt_inline"
                    ]

                    description = ""
                    for sel in desc_selectors:
                        desc_tag = news.select_one(sel)
                        if desc_tag:
                            text = desc_tag.get_text(strip=True)
                            if text:
                                description = text
                                break

                    if not description:
                        content_area = news.select_one(".cont_thumb") or news
                        full_text = content_area.get_text(separator=" ", strip=True)
                        if title and title in full_text:
                            description = full_text.replace(title, "").strip()
                        else:
                            description = full_text.strip()

                    if description:
                        description = re.sub(r".*?개별문서메뉴.*?공유하기", "", description).strip()

                    # 길이 제한
                    if description and len(description) > 300:
                        description = description[:300].rstrip() + "..."


                    news_data = {
                        "title": title,
                        "link": link,
                        "image_url" : image_url,
                        "description" : description
                    }
                    results.append(news_data)

            page += 1
            time.sleep(0.5)

        except Exception as e:
            print(f"크롤링 중 에러 발생 : {e}")
            break
            
    return results[:limit]
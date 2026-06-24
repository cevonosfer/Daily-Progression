import requests
from bs4 import BeautifulSoup
import time
import json 


data = []
for i in range(1,51):

    try:
        r = requests.get(f'https://books.toscrape.com/catalogue/page-{i}.html', timeout=10)
        r.raise_for_status()
        r.encoding = 'utf-8'
    except requests.RequestException as e:
        print(f"Failed on page {i}: {e}")
        continue    

    soup = BeautifulSoup(r.text, 'html.parser')
    books = soup.select('article.product_pod')

    for book in books:
        title = book.select_one('h3 a')['title']
        price = book.select_one('p.price_color').text
        star = book.select_one('p.star-rating')['class'][1]
        data.append({"title": title, "price": price, "star-rating":star})
    time.sleep(0.5)

with open("python/web_scraper/books.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)


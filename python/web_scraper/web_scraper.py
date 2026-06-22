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
    books = soup.find_all('article', class_='product_pod')

    for book in books:
        title = book.find('h3').find('a')['title']
        price = book.find('p', class_='price_color').text
        data.append({"title": title, "price": price})
    time.sleep(0.5)

with open("books.json", "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2, ensure_ascii=False)


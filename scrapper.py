import requests
import json
from bs4 import BeautifulSoup

# URL of the website to scrape
URL = "http://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to load page: {response.status_code}")
        return None

    # Set encoding explicitly to handle special characters
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    book_list = []

    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        currency = price_text[0]
        price = price_text[1:]

        book_list.append({
            "title": title,
            "price": price,
            "currency": currency
        })

    return book_list

books = scrape_books(URL)

if books:
    with open("books.json", "w") as f:
        json.dump(books, f, indent=2)

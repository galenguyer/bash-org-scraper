from time import sleep
import json
import sys
import requests
from bs4 import BeautifulSoup

QUOTES = {}


def get_page(pagenum: int) -> None:
    page = requests.get(f"http://bash.org/?browse&p={pagenum}")
    soup = BeautifulSoup(page.content, "html.parser")
    quotes_meta = soup.find_all("p", attrs={"class": "quote"})
    quotes = soup.find_all("p", attrs={"class": "qt"})
    for i in range(len(quotes)):
        id = int(quotes_meta[i].find_all("b")[0].text.strip("#"))
        points = int(quotes_meta[i].find_all("font")[0].text)
        quote = {}
        quote["content"] = str(quotes[i].text)
        quote["id"] = id
        quote["points"] = points
        QUOTES[id] = quote


def main():
    for i in range(1, 423):
        print(f"Scraping page {i}")
        get_page(i)
        sleep(1)
    print(json.dumps(QUOTES, indent=4))
    with open("quotes.json", "w") as fd:
        fd.write(json.dump(QUOTES, indent=4))


if __name__ == "__main__":
    main()

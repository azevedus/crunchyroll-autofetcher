import requests
from bs4 import BeautifulSoup

def mangaList_spider():
    url = 'http://m.crunchyroll.com/anime/?tab=all'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    for link in soup.findAll('span', {'class': 'series'}):
        title = link.string.encode('utf-8')
        print(title)

mangaList_spider()
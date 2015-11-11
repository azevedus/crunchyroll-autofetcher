import requests
from bs4 import BeautifulSoup

def soupCrawler(soupLink):
    global source_code, plain_text, soup
    source_code = requests.get(soupLink)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")

def mangaList_spider():

    soupCrawler('http://www.crunchyroll.com/videos/anime/alpha?group=all')
    for mangaListInfo in soup.findAll(token="shows-portraits"):
        title = mangaListInfo.string.encode('utf-8')
        link = 'http://www.crunchyroll.com' + mangaListInfo.get('href')

        print title
        print link



mangaList_spider()
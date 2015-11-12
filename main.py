import requests
from bs4 import BeautifulSoup

def soupCrawler(soupLink):
    global source_code, plain_text, soup
    source_code = requests.get(soupLink)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")

def commandLetter():

    print ("Please input the starter letter of the anime you want to download: ")
    global selectedLetter
    selectedLetter = raw_input()
    print ("")

def mangaList_spider():

    soupCrawler('http://www.crunchyroll.com/videos/anime/alpha?group='+selectedLetter)
    for leftGrid in soup.findAll('div', {'id':'main_content'}):
        i = 1
        selectedLetterList = leftGrid.findAll('span', {'class':'series-title block ellipsis'})
        for mangaListInfo in selectedLetterList:

            title = mangaListInfo.string.encode('utf-8')
            print str(i) + " - " + title
            i += 1

def selectedSeries_spider():
    print ("")
    print ("Please enter the number correspondent to the series you want to download "
           "or 'exit' to return to the previous menu")
    selectedSeries = raw_input()
    selectedSeries = str(selectedSeries)

    if selectedSeries == "exit":
        print ("")
        finalRun()
    else:
        selectedSeries = int(selectedSeries)
        selectedSeries -= 1

        for leftGrid in soup.findAll('div', {'id':'main_content'}):
            selectedLetterList = leftGrid.findAll('span', {'class':'series-title block ellipsis'})[selectedSeries].parent.parent
            selectedAnimeUrl = 'http://www.crunchyroll.com' + selectedLetterList.get('href')
            print selectedAnimeUrl

def finalRun():
    commandLetter()
    mangaList_spider()
    selectedSeries_spider()

finalRun()

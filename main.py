import requests
import html5lib
import re
from bs4 import BeautifulSoup

def soupCrawler(soupLink):
    global source_code, plain_text, soup
    source_code = requests.get(soupLink)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html5lib')

def commandLetter():

    print ("Please input the starter letter of the anime you want to download: ")
    global selectedLetter
    selectedLetter = raw_input()
    print selectedLetter
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
    global episodeNumber
    print ("")
    print ("Please enter the number correspondent to the series you want to download "
           "or '!return' to return to the previous menu")
    selectedSeries = raw_input()
    selectedSeries = str(selectedSeries)

    if selectedSeries == "!return":
        print ("")
        finalRun()
    else:
        selectedSeries = int(selectedSeries)
        selectedSeries -= 1
        print ("")

        for leftGrid in soup.findAll('div', {'id':'main_content'}):
            selectedLetterList = leftGrid.findAll('span', {'class':'series-title block ellipsis'})[selectedSeries]
            selectedAnimeTitle = selectedLetterList.string
            selectedLetterLink = selectedLetterList.parent.parent
            selectedAnimeUrl = 'http://www.crunchyroll.com' + selectedLetterLink.get('href')

            keepLoop = True

            while keepLoop == True:

                print ("You have selected " + selectedAnimeTitle + ".")
                print ("If you already now the number of the episode you want to download, "
                       "enter '!episodenumber', "
                       "'!list' for a complete list of the available episodes or "
                       "'!return' to go back to the list of series")
                selectedSeriesDecision = raw_input()
                print ("")

                if selectedSeriesDecision == "!list":

                    # Selected series page spider
                    soupCrawler(selectedAnimeUrl)
                    for episodeInfo in soup.findAll('a', {'class':'portrait-element block-link titlefix episode'}):
                        for episodeNumber in episodeInfo.findAll('span', {'class':'series-title block ellipsis'}):
                            episodeNumber = episodeNumber.string
                            episodeStrippedNumber = episodeNumber.strip()
                            print episodeStrippedNumber,
                        for episodeTitle in episodeInfo.findAll('p', {'class':'short-desc'}):
                            episodeStrippedTitle = episodeTitle.string
                            episodeStrippedTitle = episodeStrippedTitle.strip()
                            print "- " + episodeStrippedTitle

                    print("")
                    keepLoop = True

                elif selectedSeriesDecision == "!return":
                    keepLoop = True

                else:
                    soupCrawler(selectedAnimeUrl)
                    for episodeInfo in soup.findAll('a', {'class':'portrait-element block-link titlefix episode'}):
                        for episodeNumber in episodeInfo.findAll('span', {'class':'series-title block ellipsis'}):
                            episodeNumber = episodeNumber.string
                    selectedEpisodeNumber = selectedSeriesDecision.replace("!", "")
                    if selectedEpisodeNumber.isdigit():
                        selectedEpisode_spider(selectedEpisodeNumber, selectedAnimeUrl, episodeNumber)

                        keepLoop = False
                    else:
                        print ("Command unknown.")
                        print ("")
                        keepLoop = True

def selectedEpisode_spider(selectedEpisodeNumber, selectedAnimeUrl, episodeNumber):
    print "Selected anime url: " + selectedAnimeUrl
    print "Selected episode: " + selectedEpisodeNumber

    episodeNumber = episodeNumber.replace("1", selectedEpisodeNumber)

    soupCrawler(selectedAnimeUrl)
    for selectedEpisodeBlock in soup.findAll('span', {'class':'series-title block ellipsis'}):
        for selectedBlockLink in selectedEpisodeBlock.findAll(text=re.compile(episodeNumber), limit=1):
            selectedBlockLink = selectedBlockLink.parent.parent.get('href')
            print selectedBlockLink

def finalRun():
    commandLetter()
    mangaList_spider()
    selectedSeries_spider()

finalRun()

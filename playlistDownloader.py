import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("/Users/matthewszurkowski/Desktop/TheSCproject/chromedriver")
playlistName = input("Please enter the URL of your SoundCloud Playlist:\n")
try:
    driver.get(playlistName)
except:
        print("Incorrect input please try again")
        time.sleep(5)
        quit()

def collectScrollData():
    #Gets the amount of tracks in the playlist
    currentTrack = 0
    numOfTracksSelc = driver.find_element_by_xpath("//div[@class='genericTrackCount__title']")
    trackContent = numOfTracksSelc.get_attribute('innerHTML')
    numberOTrack = int(trackContent.strip())
    print("Loading Data...");
    trackProgress = 0
    while (currentTrack!=1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        get_div = driver.find_elements_by_xpath('.//span[@class = "trackItem__number sc-font"]')
        for elems in get_div:
            elems = int(elems.text)
            if (elems==numberOTrack):
                print("Complete")
                currentTrack=1
                
def collectLinks():
    #Collects the links from the site
    elements = []
    collectionProgress = 0
    elems = driver.find_elements_by_xpath("//a[@href]")
    print("Collecting links...")
    for elem in elems:
        elements.append(str(elem.get_attribute("href")))
    return elements

def sortLinks(elements, playlistName):
    #Sorts the links as best as I could
    counter = 0
    linkSorter = []
    print("Sorting links...")
    for i in elements:
        if (counter!=0):
            prev = elements[counter-1] + '/'
            lenOfPrev = len(prev)
            check = i[0:lenOfPrev]
            if (check == prev):
                linkSorter.append(i)
        counter = counter + 1
        
    for i in linkSorter:
        occCounter = linkSorter.count(i)
        lastCharsOfI = i[-4:-1]
        lastCharsOfURL = playlistName[-4:-1]
        if (lastCharsOfI!=lastCharsOfURL):
            linkSorter.remove(i)
        if (occCounter<1):
            linkSorter.remove(i)
    
    return linkSorter

def downloadLinks(links):
    linkCounter = 0
    for i in links:
        driver.get('https://sclouddownloader.net//')
        time.sleep(3)
        try:
            downloadBox = driver.find_element_by_xpath("//input[@name='sound-url']")
            downloadBox.send_keys(links[linkCounter] + '\n')
            linkCounter = linkCounter + 1
            time.sleep(4)
            downloadButton = driver.find_element_by_xpath("//*[contains(text(), 'Download Track ')]")
            time.sleep(10)
            downloadButton.click()
            time.sleep(5)
        except:
            downloadBox = driver.find_element_by_xpath("//input[@name='sound-url']")
            downloadBox.send_keys(links[linkCounter] + '\n')
            time.sleep(4)
            downloadButton = driver.find_element_by_xpath("//*[contains(text(), 'Download Track ')]")
            time.sleep(10)
            downloadButton.click()
            time.sleep(5)
        linkCounter = linkCounter + 1
               
def main(playlistName):
    driver.maximize_window()
    collectScrollData()
    elements = collectLinks()
    links = sortLinks(elements, playlistName)
    downloadLinks(links)
    driver.quit()
    
main(playlistName)

import time, os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
import findDuds as Duds

src_path = ""

def getSrcPath():
    global src_path
    startSrc = True
    while (startSrc):
        src_path = input("Please type a download location.\nExample:\n\n/Users/matthewszurkowski/Desktop/DownloadFolder\n")
        if os.path.exists(src_path):
            startSrc=False
    return src_path

def chromeSetup():
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : str(getSrcPath())}
    options.add_experimental_option('prefs', prefs)        
    driver = webdriver.Chrome("/Users/matthewszurkowski/Desktop/SoundCloud-Playlist-Downloader-master/chromedriver", options=options)
    playlistName = input("Please enter the URL of your SoundCloud Playlist:\n")
    try:
        driver.get(playlistName)
    except:
        print("Incorrect input please try again")
        time.sleep(5)
        chromeSetup()
    main(playlistName, driver)

def collectScrollData(driver):
    #Gets the amount of tracks in the playlist
    time.sleep(2)
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
    time.sleep(2)
                
def collectLinks(driver):
    #Collects the links from the site
    elements = []
    collectionProgress = 0
    elems = driver.find_elements_by_xpath("//a[@href]")
    print("Collecting links...")
    for elem in elems:
        elements.append(str(elem.get_attribute("href")))
    return elements

def sortLinks(elements, playlistName, driver):
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

def downloadLinks(links, driver):
    global src_path
    linkCounter = 0
    dudLinks = {}
    for i in links:
        driver.get('https://sclouddownloader.net//')
        time.sleep(3)
        try:
            downloadBox = driver.find_element_by_xpath("//input[@name='sound-url']")
            downloadBox.send_keys(links[linkCounter] + '\n')
            time.sleep(4)
            downloadButton = driver.find_element_by_xpath("//*[contains(text(), 'Download Track ')]")
            time.sleep(6)
            downloadButton.click()
            time.sleep(6)
            for element in driver.find_elements_by_tag_name('i'):
                if (element.text != "Download Another Track" and element.text != '"Download"' and element.text != "SoundCloud Playlist Downloader"):
                    dudLinks[element.text] = links[linkCounter]
        except:
            print("Something went wrong\n")
        linkCounter = linkCounter + 1
    newFiles = Duds.getFiles(src_path)
    checkFiles = Duds.checkDict(dudLinks)
    new_list = Duds.notMatches(newFiles, checkFiles)
    Duds.printDuds(new_list)
        
               
def main(playlistName, driver):
    driver.maximize_window()
    collectScrollData(driver)
    elements = collectLinks(driver)
    links = sortLinks(elements, playlistName, driver)
    downloadLinks(links, driver)
    driver.quit()
chromeSetup()

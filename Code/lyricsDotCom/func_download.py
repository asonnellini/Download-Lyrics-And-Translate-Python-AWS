
# This script uses Selenium - https://www.selenium.dev/documentation/en/
# "Selenium is many things but at its core, it is a toolset for web browser automation that uses the best techniques available 
# to remotely control browser instances and emulate a user’s interaction with the browser." (quote from Selenium.dev)

# Example as to how use Selenium:
# https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08


# WHY did I need selenium?
# Navigating the website lyrics.com I realized the URL address for a song may be different depending on how you land on the page 
# that has the lyrics.
# For example, both the below 2 links lead to the same web page (for the same song):
# https://www.lyrics.com/lyric/23408014
# https://www.lyrics.com/lyric/36308128/Dire+Straits/Money+for+Nothing
# Also, please note the random (i.e. I do not know how it is generated) number between /lyrics/ and /Dire+Straits/Money+for+Nothing
# Because of that random number, I cannot build directly a valid URL from the couple [name artist, name song], i.e.
# the following url does not work: https://www.lyrics.com/lyric/Dire+Straits/Money+for+Nothing
# I need to mimic the steps I would do using a browser to search for a lyrics of my interest, namely:
# - Navigate to the website www.lyrics.com
# - Search for an artist in the searchbox 
#   - Select the option "search by artist"
#   - Type the name of the artist
#   - Click on Search
# - Click on the link of the artist that matches your search
# - Search in the landing page the song of your interest (this webpage displays all songs from the artist)

############### LIBRARIES ##############
                                        
import selenium                         
from selenium import webdriver
# To manage NoSuchElementException exception from Selenium (e.g. when the html tag is not found)
from selenium.common.exceptions import NoSuchElementException
# To manage WebDriverException exception from Selenium (e.g. when the chrome driver is not found)
from selenium.common.exceptions import WebDriverException

# I needed to add in the code some "pause" to let the download of the webpage be completed
import time

# Requests and bs4 are needed to parse html content
# Requests is also needed to send POST request to Amazon API Gtw
import requests
import bs4

# To manage exit from the script due to exceptions
import sys

# manage the logging of events
import logging

# manage directory content and files
#import os
from pathlib import Path

# module to detect whether the OS is Windows, Linux or Mac
import platform

# needed to download the chrome driver file if not available
import wget

# module to zip/unzip files - needed to unzip the Chrome driver
from zipfile import ZipFile

#######################################

############## FUNCTIONS ##############

def reversed_artist_name(initial_name : str):
    """
    This function splits the input string initial_name in 2 (if initial_name is made at least of 2 words) strings 
    based on the first separator = " " (space), reverse their order and merge them in a new string.
    If initial_name is made of more than 2 words, the string is still splitted in 2 based on the first separator = " " (space)
    found in the string.

    Args:
        initial_name : string - name of the artist in input 

    Output:
        final_name : string - name of the artist after reversing the words is made of 

    Example:
        name_before = "Cent 50"
        name_after = reversed_artist_name(name_before)
        print(name_after) 
        #returns "50 Cent"

    """    
    ## check initial_name is a string; if not, convert it to string
    try:
        assert type(initial_name) == str
    except AssertionError as ex:
        initial_name = str(initial_name)

    final_name = initial_name

    splitted_words = initial_name.split(sep = " ", maxsplit = 1)

    ## reverse the order of the words only if there are at least 2 words
    if len(splitted_words) >1:
        final_name = splitted_words[1] + " " + splitted_words[0]

    return final_name


#######################################

def capital_first(word : str = None):
    """
    This function capitalize the first letter of each word in the input String.

    Args:
        word: string

    Output:
        word: string - string with first letter of each word uppercase
    
    Example:
    name_before = "dire straits"
    name_after = capital_first(name_before)
    print(name_after) 
    #returns "Dire Straits"
    """
    word = str(word)

    if word is not None:
        splitted = word.split(sep = " ")
        splitted_Capital = [i.capitalize() for i in splitted ]

        word = " ".join(splitted_Capital)

    #else:
    #    raise Exception("\ncapital_first exception: input word is None.\n")

    return word

#######################################

def detect_OS():
    """
    This function detects the OS where the script is running.
    If the function is not able to detect any OS, the function asks the user to type a valid OS type.
    In case an invalid OS is entered, the function raises an exception and shuts down the program.

    Output:
        OS_type - Possible values (note they are all lower case):
                    - windows
                    - linux
                    - macos
    """
    OS_type = platform.system()

    OS_type = OS_type.lower()

    if OS_type == "darwin":
        OS_type = "macos"


    if OS_type == "":
            logging.warning("""The program could not detect the OS type - 
            please enter the name of your OS type.\nValid OS types are (case insensitive):\n
            \tWindows\n
            \tMacOS\n
            \tLinux""")
            
            OS_type = input().lower()
            
            try:
                assert (OS_type == "windows" or OS_type == "macos" or OS_type == "linux")
            except AssertionError as aExc:
                logging.critical("The OS you entered is not supported.")
                input("Press enter to exit the program...")
                sys.exit()

    return OS_type

#######################################

def get_chrome_driver_filename(OS_type:str):
    """
    This function returns the name of the chrome driver file depending on the OS where the program is running.
    Args:
        OS_type - Possible values (note they are all lower case):
                    - windows
                    - linux
                    - macos

    Output:
        chrome_driver_filename - Possible values:
                                    - chromedriver.exe (for windows OS)
                                    - chromedriver (for MacOS or Linux)
    """

    if OS_type == "windows":
        chrome_driver_filename = "chromedriver.exe"

    elif OS_type == "linux" or OS_type == "macos":
        chrome_driver_filename = "chromedriver"

    return chrome_driver_filename

#######################################

def download_chrome_driver(auto_download : str, current_dir : Path, OS_type : str):
    """
    If auto_download = "y" this function attempts to download the Chrome Driver
    file compatible with the current OS and with Chrome 84.
    The file is stored in the current working directory.

    Args:
        auto_download - If set to y, the function downloads the file; if set to n, the function returns an error message and exits the program
        current_dir - Current working directory Path
        OS_type - OS type (e.g. windows, macos, linux)

    Output:
        final_chrome_location - Path which points to the location where the chrome driver file is located

    """

    if auto_download.lower() == "y":


        if OS_type == "windows":
            link = "https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_win32.zip"

        elif OS_type == "linux":
            link = "https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_linux64.zip"

        elif OS_type == "macos":
            link = "https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_mac64.zip"
                    

        try:
            logging.info(f"Start download of ChromeDriver for Chrome 84 on {OS_type}.")
            dwld_chrome_driver = wget.download(link)
        except Exception as ex_download:
                    
            logging.critical("Could not download the ChromeDriver file.")
            logging.critical("Please download it manually and retry entering the ChromeDriver path using the input variable 'chrome' in the method .download().")
            logging.critical("E.g.:")
            logging.critical("\t instanceSongLyric.download(chrome = 'C:\chrome_driver_selenium\chromedriver.exe')")
            logging.critical("For further information on ChromeDriver, please visit https://sites.google.com/a/chromium.org/chromedriver/getting-started.\n")
            logging.critical("Closing the program passing the original exception: {0}\n{1}".format(type(ex_download).__name__, ex_download.args))
            sys.exit(ex_download)

        try:
            with ZipFile(dwld_chrome_driver, 'r') as zipObj:
                logging.info("Download completed.")
                # Extract all the contents of zip file in current directory
                zipObj.extractall()
                #need to check the name of the file in the zip because depending on the OS it may be different
                driver_name = zipObj.namelist()[0]
        except Exception as ex_unzip:
            logging.critical("Could not unzip the ChromeDriver file.")
            logging.critical("Please unzip it manually and retry entering the ChromeDriver path using the input variable 'chrome' in the method .download().")
            logging.critical("E.g.:")
            logging.critical("\t instanceSongLyric.download(chrome = 'C:\chrome_driver_selenium\chromedriver.exe')")
            logging.critical("For further information on ChromeDriver, please visit https://sites.google.com/a/chromium.org/chromedriver/getting-started.\n")
            logging.critical("Closing the program passing the original exception: {0}\n{1}".format(type(ex_unzip).__name__, ex_unzip.args))
            sys.exit(ex_unzip)

        final_chrome_location = current_dir / driver_name

    elif auto_download.lower() == "n":
            
        logging.critical("Please enter a valid ChromeDriver path using the input variable 'chrome' in the method .download().")
        logging.critical("E.g.:")
        logging.critical("\t instanceSongLyric.download(chrome = 'C:\chrome_driver_selenium\chromedriver.exe')")
        logging.critical("For further information on ChromeDriver, please visit https://sites.google.com/a/chromium.org/chromedriver/getting-started.\n")
        logging.critical("Closing the program passing the original exception: {0}\n{1}".format(type(ex).__name__, ex.args))
        sys.exit(ex)
    #to improve to consider the case where the user neither select y/n

    return final_chrome_location

#######################################

def launch_chromium(chrome_location : str = None, debugLevel : str = 'INFO'):
    """
    This function launch a chrome instance using Selenium suite.
    NOTE: This function requires a valid path to ChromeDriver to be set in PATH, or passed as input parameter (chrome_location).

    Args:
        chrome_location: string - path pointing to the location of the chrome driver

        debugLevel: string - debug level; values:
            DEBUG          : Maximum level of debug, in addition to the same traces available for level INFO, 
                             Chrome is started with graphical interface 
            INFO (default) : Chrome is started with no graphical interface
            WARNING        : Chrome is started with no graphical interface and only warning or more critical messages are displayed

        

    Output:
        driver_chrome: webdriver object to launch chrome

    """
    
    # When launching Selenium webdriver (see webdriver.Chrome command few lines below), 
    # a "managed" instance of Chrome is open and displayed on video.
    op = webdriver.ChromeOptions()

    #disable browser non-fatal warnings
    op.add_argument('log-level=3') 

    if debugLevel != 'DEBUG':
        #disable the graphical interface of the browser
        op.add_argument('headless') 
        
        # the below 2 options are needed when running in headless mode to ensure all relevant tags 
        # are loaded and "visible" to the browser
        op.add_argument('start-maximized')
        op.add_argument("window-size=1920,1080")
        # Other switches at the below link:
        #https://peter.sh/experiments/chromium-command-line-switches/

    #detect current working dir
    current_dir = Path.cwd()

    if (chrome_location is None): 
        #if no chrome driver location is passed, the program tries to use PATH variable;
        #if no chrome driver location is set in the PATH variables, then it tries to detect it
        #in the current wrk dir
        #if no chrome driver is available in the wrk dir, the program attempts to download it
        # assuming Chrome v. 84 is installed in the system

        OS_type = detect_OS()

        chrome_driver_name = get_chrome_driver_filename(OS_type)

        if not(Path(current_dir / chrome_driver_name).exists()): #and ("chromedriver.exe" not in os.listdir(current_dir)): #
       
            #webdriver.Chrome will look for ChromeDriver path into the PATH variable 
            logging.warning(f"Neither any explicit path for chromedriver was passed nor {chrome_driver_name} is available in the current working directory ({current_dir})\nTrying to retrieve it from the PATH environment variable....")
            
            try:
                # Launch Chrome to access web 
                driver_chrome = webdriver.Chrome(options=op)

            except WebDriverException as ex:
                logging.critical("The script could not find a valid ChromeDriver path.")
                logging.critical(f"The program can attempt to download the ChromeDriver for Chrome v. 84 automatically in the current working directory ({current_dir})")
                logging.critical("Would you like to download it? (y/n) ")
                auto_download = input()
            
                chrome_location = download_chrome_driver(auto_download, current_dir, OS_type)
    
        elif Path(current_dir / chrome_driver_name).exists(): #"chromedriver.exe" in os.listdir(current_dir): #

            chrome_location = current_dir  /  chrome_driver_name

    elif (chrome_location is not None):
        #Create a Path object for the chrome_location ==> this should ensure compatibility 
        #with any format of the path (Win/Lin/MacOS)
        chrome_location = Path(chrome_location)


    if str(chrome_location.resolve()) is not None: 
        
        try:
            # Launch Chrome to access web 
            driver_chrome = webdriver.Chrome(str(chrome_location.resolve()), options=op)
            # To improve: need to find a way to ensure this scritp can be run by someone who does not have the webdriver,
            # or has it in a non standard location

        except WebDriverException as ex:
            logging.critical("The script could not launch a chrome instance, this might be due to a wrong chromedriver path.\n")
            logging.critical("The chromedriver path you typed is {0}.\nPlease check whether it is valid.".format(chrome_location))
            logging.critical("ChromeDriver path can be passed via the input variable 'chrome' in the method .download().")
            logging.critical("E.g.:")
            logging.critical("\t instanceSongLyric.download(chrome = 'C:\chrome_driver_selenium\chromedriver.exe')\n")
            logging.critical("For further information about chromedriver, please visit https://sites.google.com/a/chromium.org/chromedriver/getting-started.\n")
            logging.critical("Closing the program passing the original exception: {0}\n{1}".format(type(ex).__name__, ex.args))
            sys.exit(ex)
    
    return driver_chrome

#######################################

def download_song(artist:str = None, song:str = None, chrome:str = None, debugLevel:str = 'INFO'):
    """
    This function downloads from lyrics.com the lyric of the song specified as input.

    Args:
        artist: string - name of the artist; default = None

        song: string - name of the song; default = None

        chrome_location: string - path pointing to the location of the chrome driver

        debugLevel: str - debug level; values:
            DEBUG          : Maximum level of debug, in addition to the same traces available for level INFO, 
                             Chrome is started with graphical interface 
            INFO (default) : Chrome is started with no graphical interface
            WARNING        : Chrome is started with no graphical interface and only warning or more critical messages are displayed


    Output:
        result:  list

        Errordetail: int - not implemented yet

    """

    ########## SAFETY CHECKS AND PREPROCESSING ###########

    #Usage of getattr: getattr(logging, debugLevel) is identical to logging.debugLevel

    debugLevel = debugLevel.upper()

    logging.basicConfig(format='%(levelname)s:%(message)s', level= getattr(logging, debugLevel)  )

    try:
        assert type(artist) == str
    except AssertionError as ex:
        artist = str(artist)

    try:
        assert type(song) == str
    except AssertionError as ex:
        song = str(song)

    # ensure the first letter of each word of the string is Capital Letter, i.e. same formatting used on lyrics.com
    artist = capital_first(artist)
    song = capital_first(song)

    logging.info("Starting the search of the lyric of the song '{0}' from '{1}' on www.lyrics.com".format(song, artist))

    ########## OPEN THE BROWSER ###########

    # Launch Chrome to access web
    logging.info("Launching a Chrome instance driven by Selenium.")
    driver = launch_chromium(chrome, debugLevel) 
    logging.info("Chrome instance driven by Selenium successfully launched.")
    # NOTE: need to find a way to ensure this scritp can be run by someone who does not have the webdriver,
    # or has it in a non standard location

    # Open the website
    logging.info("Opening www.lyrics.com")
    driver.get('https://www.lyrics.com/')


    ### SEARCH THE NAME OF THE ARTIST IN THE WEBSITE ###

    #search "by Artist" option in the upper search bar:
    #<label for="page-word-search-op2"><span>By Artist</span></label>
    try:
        option_search_by_artist_button = driver.find_element_by_css_selector("label[for='page-word-search-op2']")
    except NoSuchElementException as ex:
        logging.error("The tag 'label[for='page-word-search-op2']' was not found in the web page {0}.\n".format( driver.current_url))
        logging.error("This could be due to: \n\t\n\tPage not reachable or not fully loaded\n\tThe page being modified\n".format( driver.current_url))
        logging.error("You may want to inspect the page manually: {0}".format( driver.current_url))
        logging.error("Closing the program passing the original exception: {0}\n{1}".format(type(ex).__name__, ex.args))
        sys.exit(ex)

    option_search_by_artist_button.click()

    # Search box:
    #<input id="search" type="text" class="page-word-search-query rc5 ui-autocomplete-input" name="st" value="" placeholder="Search for lyrics or artists..." autocomplete="off">
    try:
        id_box = driver.find_element_by_id('search')
    except NoSuchElementException as ex:
        logging.error("The Lyrics Search Box was not found in the web page {0}.".format( driver.current_url))
        logging.error("This could be due to: \n\t\n\tPage not reachable or not fully loaded\n\tThe page being modified\n")
        logging.error("You may want to inspect the page manually: {0}".format( driver.current_url))
        logging.error("Closing the program passing the original exception: {0}\n{1}".format(type(ex).__name__, ex.args))
        sys.exit(ex)

    # Type in the Search box the name of the artist
    id_box.send_keys(artist)

    # Search button
    #<button type="submit" class="btn primary" id="page-word-search-button">Search</button>
    try:
        search_button = driver.find_element_by_id('page-word-search-button')
    except NoSuchElementException as ex:
        logging.error("The Search button was not found in the web page {0}.".format( driver.current_url))
        logging.error("This could be due to: \n\t\n\tPage not reachable or not fully loaded\n\tThe page being modified\n")
        logging.error("You may want to inspect the page manually: {0}".format( driver.current_url))
        logging.error("Closing the program passing the original exception: {0}\n{1}".format(type(ex).__name__, ex.args))
        sys.exit(ex)

    # Click search
    search_button.click()
    logging.info("Searching the artist: {0}.".format(artist))

    # "pause" to ensure the new page is fully loaded
    time.sleep(3)

    #Select the link that includes in the "title" attribute the name of the artist
    #<a class="name" href="artist/Dire-Straits/4101" title="Dire Straits">Dire Straits</a>
    try:
        artist_link = driver.find_element_by_css_selector('a[class="name"][title="'+ artist + '"]')
    except NoSuchElementException as ex:
    
        try:
            # If the name of the band is made of 2 or more words, it might worth to reverse their order and retry
            artist = reversed_artist_name(artist)
            artist_link = driver.find_element_by_css_selector('a[class="name"][title="'+ artist + '"]')
        except NoSuchElementException as ex:  
            logging.error("The artist name was not found in the web page {0}. \nThis could be due to: \n\tThe page not being completely loaded\n\tThe page being modified\n\tA mismatch between the artist name you typed and the artist name in www.lyrics.com".format( driver.current_url))
            logging.error("You may want to inspect the page manually: {0}".format(driver.current_url))
            logging.error("Closing the program passing the original exception: {0}\n{1}".format(type(ex).__name__, ex.args))
            sys.exit(ex)

    artist_link.click()
    logging.info("Artist found.")

    # "pause" to ensure the new page is fully loaded
    time.sleep(2)

    #######################################


    ### SEARCH THE SONG AMONG THOSE AVAILABLE FOR THE ARTIST ###

    #Select the link that contains the name of the song in it

    # Possible enhancement:
    # - parse all the links available that contains the name of the song + other words
    # - select the link which is most similar (but not necessarily identical) to the song typed by the user
    logging.info("Searching the song: {0}.".format(song))
    try:
        song_link = driver.find_element_by_link_text(song)
    except NoSuchElementException as ex:
        logging.error("The song was not found in the web page {0}. \nThis could be due to: \n\tThe page not being completely loaded\n\tThe page being modified\n\tA mismatch between the song name you typed and the song name in www.lyrics.com".format( driver.current_url))
        logging.error("You may want to inspect the page manually: {0}".format( driver.current_url))
        logging.error("Closing the program passing the original exception: {0}\n{1}".format(type(ex).__name__, ex.args))
        sys.exit(ex)

    song_link.click()
    logging.info("Song found.")

    url_request = requests.get(driver.current_url)

    ########## EXTRACT THE LYRIC ##########

    logging.info("Extracting the lyric.")

    # the below 2 lines are needed because in the html page the text is mixed with links, e.g.
    # <pre> lyric part1 <a href = www.example.com> lyric part2  <\a> lyric part3  <\pre>
    soup = bs4.BeautifulSoup(url_request.text, 'lxml') # This requires package lxml
    downloaded_lyric = [p.text for p in soup.findAll('pre')] 

    driver.quit()

    logging.info("Lyric extracted.")

    return downloaded_lyric[0]

def translate_song(input_lyric:str, target_lang:str = "it"):
    """
    This function translates the input_lyric text in the language specified by the code of target_lang.
    It will work only if the amazon gateway API is up and running.

    Args.:
        input_lyric: str - text to be translated
        target_lang: str - target language code; allowed code values on: https://docs.aws.amazon.com/translate/latest/dg/what-is.html#what-is-languages

    """
    dict_to_translate = '{"sourceText":"' + input_lyric.replace("\n"," ;; ").replace('"',' ') + ' ","lang":"' + target_lang + '"}'
    newHeaders = {'Content-type': 'application/json'}
    response = requests.post('https://2zzv2bm234.execute-api.us-east-1.amazonaws.com/dev/translate', data=dict_to_translate,headers=newHeaders)

    return response.json()["body"].replace(" ;; ","\n")




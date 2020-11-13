# Release notes LyricsDotCom

# 06 August 2020

## Overview

The library LyricsDotCom allows you to: 
- download the lyric of a song from the website www.lyrics.com
- translate the lyric to a target language using AWS translate service (using an API Gtw and a Lambda functions)
- create a library of artists and songs

For an example of usage, please refer to the section "Demo".

Before using LyricsDotCom, please read the "Requirements" and "Known Limitations" sections of this Release Notes.

## New features

- Translate a lyric from English to any language via AWS translate service
- New class LibrarySong to store multiple songs and search them by artist, song or both
- Automatic download of the Chrome Driver file for Chrome v. 84, see also Requirements section
- Replace "print" with "logging" commands
- Re-organize file/folder structure and added a \_\_init\_\_.py
- Enhanced management of folders path to ensure compatibility with MacOS and Linux (TO BE TESTED)


## Classes and methods

- class SongLyric
	- Attributes:
		- artist: string
		- song: string
		- lyric: string
		- lang: string - language code to translate the lyrics to
        - translated_lyric: string - translated lyrics

	- Methods:
		- \_\_init\_\_( self, artist:str = None, song:str = None, lyric:str = None, anotherSongLyric:object = None  ) : it requires at least one input value among artist and song; if an object of class SongLyric is passed, then it creates a copy of it; please see the Section Demo
		- set\_artist(self, new_artist:str = None)
		- set\_song(self, new_song:str = None)
		- set\_lyric(self, new_lyric:str = None)
		- get\_artist(self)
		- get\_song(self)
		- get\_lyric(self)
		- download(self, chrome:str = None, debug = 'INFO')
		- translate(self, target_lang:str = "it")

- class LibrarySong
	- Attributes:
		- list_song_lyric: list

	- Methods:
		- \_\_init\_\_(self)
		- add_song(self, instance_song_lyric: SongLyric)
		- \_\_iter\_\_(self)
		- retrieve_by_song(self, song_name:str, returned_values:int = 3)
		- retrieve_by_artist(self, artist_name:str, returned_values:int = 3)
		- retrieve_by_artist_and_song(self, artist_name:str, song_name:str, returned_values:int = 3)
		- retrieve_song_by_index(self, song_position)
		

## Demo

### Import the package
import lyricsDotCom as ldc

### Create an object of the class SongLyric 
#### Either artist or song must be string different than None, lyric is optional
testSong = ldc.SongLyric(artist = "timberlake Justin", song = "cry me a river", lyric = "test lyric")

#### The constructor automatically set to upper-case the first letter of the words of the attributes artist and song  to be compliant with www.lyrics.com format
print(testSong.get\_artist()) # returns Timberlake Justin

print(testSong.get\_lyric()) # returns test lyric

print(testSong.get\_song()) # returns Cry Me A River

### "set"-like and "get"-like methods
#### You can use the "set" methods to manipulate the values of single attributes, and the "get" methods to get the values, e.g.:
testSong.set\_artist("dire Straits")

print(testSong.get\_artist()) # returns Dire Straits

### Create an instance of SongLyric by copy
#### Create an instance testSong2 of the class SongLyric copying another instance testSong: each attribute from testSong is copied to the corresponding attribute of testSong2
testSong2.ldc.SongLyric(anotherSongLyric = testSong)

#### the same will happen even if you omit the parameter anotherSongLyric:
testSong3.ldc.SongLyric(testSong)

### Download a lyric from www.lyrics.com
#### To download a lyric from www.lyrics.com there are 2 possible scenarios: Chrome Driver already available in your system as opposed to Chrome Driver not available in your system.
1. First Scenario: Chrome Driver already available in your systemcase:

	1.1. Check where your chromedriver.exe is located and store its path in a variable (see also the Requirement session)
	
	chrome\_location = "D:\chrome\_driver\_selenium\chromedriver.exe"

	1.2. Create an object SongLyric that has the artist and song of your interest: both attributes are strictly necessary
	
	testSong = ldc.SongLyric(artist = "timberlake Justin", song = "cry me a river")

	1.3. Apply the download method passing the chrome location
	
	testSong.download(chrome\_location)

	1.4. Once the download is completed, the lyric downloaded from www.lyrics.com is stored in the attribute "lyric""
	
	print(testSong.get\_lyric())

2. Second scenario: Chrome Driver not available in your system:

	2.1. Create an object that has the artist and song of your interest: both attributes are strictly necessary
	
	testSong = ldc.SongLyric(artist = "timberlake Justin", song = "cry me a river")

	2.2. Apply the download method without passing the chrome location; the program will check if any Chrome driver is available in the PATH or in the working directory. If no Chrome driver is found, the program will ask you confirmation whether it could try to download the Chrome driver for Chrome version 84. If you accept the Chrome Driver will be downloaded and the program will continue as in the First Scenario
	testSong.download()

	testSong.download()

### Translate a lyric
#### You can call the method "translate" on an instance of SongLyric that has a lyric and specify the code of the target language for the translation. For a complete list of codes, please visit https://docs.aws.amazon.com/translate/latest/dg/what-is.html#what-is-languages. 
#### Note: if the instance has no lyric, the program will return an error.

testSong.translate("it")

### Create a library of songs
#### Consider multiple instances of SongLyric

testSong = ldc.SongLyric(artist = "timberlake Justin", song = "cry me a river")

testSong2 = ldc.SongLyric(artist = "dire straits", song = "sultans of swing", lyric = "test lyric2")

testSong3 = ldc.SongLyric(artist = "50 cent", song = "in da club", lyric = "test lyric3")

#### Create an instance of LibrarySong

library = ldc.LibrarySong()

#### Add songs to the LibrarySong instance

library.add_song(testSong)

library.add_song(testSong2)
	
library.add_song(testSong3)

#### You can iterate over the elements of the library

for i in library_song:

		print(i[1]) # it will return artist name
		print(i[2]) # it will return song name
		print(i[3]) # it will return the lyric
		print(i[4]) # it will return the translated lyric
		print(i[5]) # it will return the language of the translated lyric

### Search for a song among those stored in the LibrarySong object
#### You can search among the songs stored in library by song, or artist or both; all these methods will return a list with the matches of the search:

print(library_song.retrieve_by_song("in da club"))
	
print(library_song.retrieve_by_artist("50 cent"))

print(library_song.retrieve_by_artist_and_song("50 cent", "in da club"))

#### The above search-methods support an input parameter named argument returned\_values. This input parameter is an integer and can take 3 different values: 3 (default), 4 or 5. Specifically: 3 (default) return a list having position, Artist name, Song Name; 4 is same as 3 plus the lyric; 5 same as 4 plus the translated lyric :

print(library_song.retrieve_by_artist("dire straits", 5)) # it returns all songs from Dire Straits, showing for each of them: 
- their position in library_song
- the artist name
- the song
- the lyric
- the translated lyric

## Requirements

- To use LyricsDotCom:
	- Place the folder lyricsDotCom in the working directory where your python script runs
	- Import the module lyricsDotCom via:
	
	import lyricsDotCom as ldc
	

- Chrome driver: LyricsDotCom uses Chromedriver via Selenium to navigate www.lyrics.com. This driver requires Chrome to be already installed in your system.
	The driver: 
	- Can be downloaded from this link: https://chromedriver.chromium.org/downloads
	- Should be stored in a folder that is accessible to the python user who uses LyricsDotCom
	- The path of this folder has to be passed to the method "download" which downloads the lyric, please see the Demo section for an example
		- If no path is passed explicitly to the method: 
			- The library will both try to retrieve the path from the PATH environment variable and/or check if it is in your current working directory 
			- If driver is still not found, the library will attempt to download it automatically for Chrome v. 84 upon your confirmation.


- Python libraries:
	- lxml
	- selenium                         
	- time
	- requests
	- bs4
	- sys
	- logging
	- pathlib
	- platform
	- wget
	- zipfile

## Known Limitations

LyricsDotCom may fail to download the lyric within the following scenarios:
- Slow internet connection
- Mismatch between the name of the artist/song entered by the user and the one used on www.lyrics.com

The translation of the lyric will fail if the text to be translated has special characters that cannot be formatted properly in the JSON.

The library is not managing yet certain "critical" scenarios, like for example errors that AWS translate service may return.


# 22 July 2020

### Overview

The library LyricsDotCom allows you to download the lyric of a song from the website www.lyrics.com.

For an example of usage, please refer to the section "Demo".

Before using LyricsDotCom, please read the "Requirements" and "Known Limitations" sections of this Release Notes.

### Classes and methods

- class SongLyric
	- Attributes:
		- artist: string
		- song: string
		- lyric: string

	- Methods:
		- \_\_init\_\_() : it requires at least one input value among artist and song; if an object of class SongLyric is passed, then it creates a copy of it; please see the Section Demo
		- set\_artist(<string>)
		- set\_song(<string>)
		- set\_lyric(<string>)
		- get\_artist()
		- get\_song()
		- get\_lyric()
		- download(chrome = <path of chromedriver.exe>)

### Demo


import lyrics\_dot\_com as ldc

#### Create an object of the class SongLyric (either artist or song must be string different than None, lyric is optional)
testSong = ldc.SongLyric(artist = "timberlake Justin", song = "cry me a river", lyric = "test lyric")

#### The constructor automatically set the first letter of the words of the attributes artist 
#### and song to upper-case to be compliant with www.lyrics.com format
print(testSong.get\_artist()) # returns Timberlake Justin
print(testSong.get\_lyric()) # returns test lyric
print(testSong.get\_song()) # returns Cry Me A River

#### You can use the "set" methods to manipulate the values of single attributes, and the get" methods  to get the values, e.g.:
testSong.set\_artist("dire Straits")
print(testSong.get\_artist()) # returns Dire Straits

#### Create an instance testSong2 of the class SongLyric copying another instance testSong: each attribute from testSong is copied to the corresponding attribute of testSong2
testSong2.ldc.SongLyric(anotherSongLyric = testSong)
#### the same will happen even if you omit the parameter anotherSongLyric:
testSong3.ldc.SongLyric(testSong)

#### To download a lyric from www.lyrics.com:
#### 1 - Check where your chromedriver.exe is located and store its path in a variable (see also the Requirement session)
chrome\_location = "D:\chrome\_driver\_selenium\chromedriver.exe"
#### 2 - Create an object that has the artist and song of your interest: both attributes are strictly necessary
testSong = ldc.SongLyric(artist = "timberlake Justin", song = "cry me a river")
#### 3 - Apply the download method passing the chrome location
testSong.download(chrome\_location)
#### 4 - Once the download is completed, the attribute lyrics will have the lyric downloaded from www.lyrics.com
print(testSong.get\_lyric())





### Requirements

- To use LyricsDotCom:
	- Both the files lyrics_dot_com.py and func_download.py has to be placed in the current python working directory
	- Import the classes from lyrics_dot_com.py in your script, e.g.
	
	import lyrics_dot_com as ldc
	

- Chrome driver: LyricsDotCom uses Chromedriver via Selenium to navigate www.lyrics.com.
	The driver: 
	- Can be downloaded from this link: https://chromedriver.chromium.org/downloads
	- Should be stored in a folder that is accessible to the python user who uses LyricsDotCom
	- The path of this folder has to be passed to the method "download" which downloads the lyric, please see the Demo section for an example
		- If no path is passed explicitly to the method, the library will try to retrieve the path from the PATH environment variable. 


- Python libraries:
	- lxml
	- selenium                         
	- time
	- requests
	- bs4
	- sys

### Known Limitations

LyricsDotCom may fail to download the lyric within the following scenarios:
- Slow internet connection
- Mismatch between the name of the artist/song entered by the user and the one used on www.lyrics.com

## 14 July 2020

### Overview

The library LyricsDotCom allows you to download the lyric of a song from the website www.lyrics.com.

For an example of usage, please refer to the section "Demo".

Before using LyricsDotCom, please read the "Requirements" and "Known Limitations" sections of this Release Notes.

### Classes and methods

- class SongLyric
	- Attributes:
		- artist: string
		- song: string
		- lyric: string

	- Methods:
		- `__init__()` : it requires at least one input value among artist and song; if an object of class SongLyric is passed, then it creates a copy of it; please see the Section Demo
		- `set_artist(<string>)`
		- `set_song(<string>)`
		- `set_lyric(<string>)`
		- `get_artist()`
		- `get_song()`
		- `get_lyric()`
		- `download(chrome = <path of chromedriver.exe>)`

### Demo

```
import Class as cls

# Create an object of the class SongLyric (either artist or song must be string different than None, lyric is optional)
testSong = cls.SongLyric(artist = "timberlake Justin", song = "cry me a river", lyric = "test lyric")

# The constructor automatically set the first letter of the words of the attributes artist 
# and song to upper-case to be compliant with www.lyrics.com format
print(testSong.get_artist()) # returns Timberlake Justin
print(testSong.get_lyric()) # returns test lyric
print(testSong.get_song()) # returns Cry Me A River

# You can use the set methods to manipulate the values of single attributes, 
# and the methods get to get the values, e.g.:
testSong.set_artist("dire Straits")
print(testSong.get_artist()) # returns Dire Straits

# Create an instance testSong2 of the class SongLyric copying another instance testSong:
# each attribute from testSong is copied to the corresponding attribute of testSong2
testSong2.cls.SongLyric(anotherSongLyric = testSong)
# the same will happen even if you omit the parameter anotherSongLyric:
testSong3.cls.SongLyric(testSong)

# To download a lyric from www.lyrics.com:
# 1 - Check where your chromedriver.exe is located and store its path in a variable (see also the Requirement session)
chrome_location = "D:\chrome_driver_selenium\chromedriver.exe"
# 2 - Create an object that has the artist and song of your interest: both attributes are strictly necessary
testSong = cls.SongLyric(artist = "timberlake Justin", song = "cry me a river")
# 3 - Apply the download method passing the chrome location
testSong.download(chrome_location)
# 4 - Once the download is completed, the attribute lyrics will have the lyric downloaded from www.lyrics.com
print(testSong.get_lyric())

```

### Requirements

- To use LyricsDotCom:
	- Both the files Class.py and Functions.py has to be placed in the current python working directory
	- Import the classes from Class.py in your script, e.g.
	```
	import Class as cls
	```

- Chrome driver: LyricsDotCom uses Chromedriver via Selenium to navigate www.lyrics.com.
	The driver: 
	- Can be downloaded from this link: https://chromedriver.chromium.org/downloads
	- Should be stored in a folder that is accessible to the python user who uses LyricsDotCom
	- The path of this folder has to be passed to the method "download" which downloads the lyric, please see the Demo section for an example
		- If no path is passed explicitly to the method, the library will try to retrieve the path from the PATH environment variable. 


- Python libraries:
	- lxml
	- selenium                         
	- time
	- requests
	- bs4
	- sys

### Known Limitations

LyricsDotCom may fail to download the lyric within the following scenarios:
- Slow internet connection
- Mismatch between the name of the artist/song entered by the user and the one used on www.lyrics.com




## 12 July 2020

### Requirements

Chromium driver
https://chromedriver.chromium.org/downloads

Python libraries:
- lxml
- selenium                         
- time
- requests
- bs4
- sys


## Features

- Download a lyric from lyrics.com

## Known limitations

- no exception management
- no object-oriented design
- no engineering of the software (i.e. all in one script with no functions)

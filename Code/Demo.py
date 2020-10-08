import lyricsDotCom as ldc




def main():

	# Test the set and get methods
	testSong = ldc.SongLyric(artist = "timberlake Justin", song = "cry me a river", lyric = "test lyric")

	print(testSong.get_artist())
	print(testSong.get_lyric())
	print(testSong.get_song())

	testSong1 = ldc.SongLyric("timberlake Justin")

	testSong1.set_artist("50 cent")
	print(testSong1.get_artist())

		
	# Test the download and translate method
	
	testSong = ldc.SongLyric(artist = "timberlake Justin", song = "cry me a river")

	testSong2 = ldc.SongLyric(artist = "dire straits", song = "sultans of swing", lyric = "test lyric2")
	
	# Specify the chrome driver location
	chrome_location = "D:\programmi\chrome_driver_selenium\chromedriver.exe"

	testSong2.download(chrome_location)

	testSong2.translate()

	testSong3 = ldc.SongLyric(artist = "50 cent", song = "in da club", lyric = "test lyric3")

	testSong4 = ldc.SongLyric(artist = "dire straits", song = "brothers in arms")

	testSong4.download(chrome_location)
	testSong4.translate()
	
	# test the LybrarySong library
	library_song = ldc.LibrarySong()

	library_song.add_song(testSong)

	library_song.add_song(testSong2)
	
	library_song.add_song(testSong3)

	library_song.add_song(testSong4)

	#Search song/artist in the LybrarySong object
	print(library_song.retrieve_by_song("in da club"))
	
	print(library_song.retrieve_by_artist("dire straits",3))

	print(library_song.retrieve_by_artist_and_song("50 cent", "in da club"))
	

	#iterate over the LibrarySong object to retrieve artist, song, lyric
	for i in library_song:

		print(i[1]) # artist
		print(i[2]) # song
		print(i[3]) # lyric



if(__name__ == "__main__"):

	main()


#######################################

# Other resources 
# https://www.thepythoncode.com/article/using-proxies-using-requests-in-python

# https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/

#Other info
# https://github.com/mracos/python-azlyrics

#az.normalize_str(str) (Make the str valid (no special chars, spaces, lowercase)
#az.normalize_artist_music() (Translate the artist and the music to be valid in the url below)

#az.url() (Generate a valid azlyrics url from the artist and music suplied in the creation)
#def url(self):
#        if not self.artist and not self.music:
#            self.artist = "rickastley"
#            self.music = "nevergonnagiveyouup"
#        return "http://azlyrics.com/lyrics/{}/{}.html".format(*self.normalize_artist_music())


#az.get_page() (fetch the page from the upper url)
#def get_page(self):
#        try:
#            page = urllib.request.urlopen(self.url())
#            return page.read()
#        except urllib.error.HTTPError as e:
#            if e.code == 404:
#                print("Music not found")
#                sys.exit(1)


#az.extract_lyrics(page) (extract the lyrcs from the upper page a valid azlyrics page)
#def extract_lyrics(self, page):
#        soup = BeautifulSoup(page, "html.parser")
#        lyrics_tags = soup.find_all("div", attrs={"class": None, "id": None})
#        lyrics = [tag.getText() for tag in lyrics_tags]
#        return lyrics


#az.get_lyrics() does everything above
#def get_lyrics(self):
#        page = self.get_page()
#        lyrics = self.extract_lyrics(page)
#        return lyrics


#az.format_lyrics(lyrics) (return the lyric formated to print)
#def format_lyrics(self, lyrics):
#        formated_lyrics = "\n".join(lyrics)
#        return formated_lyrics
##########################################

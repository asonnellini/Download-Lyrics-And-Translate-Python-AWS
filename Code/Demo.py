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


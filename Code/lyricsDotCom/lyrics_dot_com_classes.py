import lyricsDotCom.func_download as fd




############ CLASS SongLyric ############

class SongLyric():
    """
    SongLyric class store artist name, song name and lyric.
   
    Attributes:
        - artist: string 
        - song: string 
        - lyric: string
        - lang: string - language code to translate the lyrics to
        - translated_lyric: string - translated lyrics
    """

    def __init__(self, artist:str = None, song:str = None, lyric:str = None, anotherSongLyric:object = None ):

        if type(artist) == SongLyric:
            # If the constructor receives as input parameter an object SongLyric without specifying any flag
            # (artist, song, lyric, anotherSongLyric), it will be considered as an anotherSongLyric
            # This allows to implement a quick mechanism to copy the content of one object to another
            anotherSongLyric = artist
            artist = None

        # an object SongLyric must have at least 1 valid value for either artist or song
        if(anotherSongLyric is None ):
            #anotherSongLyric is None so we are not constructing by copy
            if (artist is not None or song is not None):
                # Using capital_first because that is the format required by www.lyrics.com
                self.artist = fd.capital_first( str(artist))
                self.song = fd.capital_first(str(song))
            else:
                raise Exception("Cannot create the instance of SongLyric: both artist and song cannot be None at the same time")

            self.lyric = str(lyric)

        else:
            #Constructing by copy
            self.artist = anotherSongLyric.artist
            self.song = anotherSongLyric.song
            self.lyric = anotherSongLyric.lyric
        
        # these 2 attributes can be set only when calling the method .translate()
        self.lang = None
        self.translated_lyric = None

##################### METHODS #####################
    
    def set_artist(self, new_artist:str = None):
        """
        This method allows you to change the value of the attribute artist.
        """
        if (new_artist is not None):
            self.artist = fd.capital_first(str(new_artist))
        else:
            raise Exception("No artist was typed in the method set_artist(). Please type one and retry.")

    def set_song(self, new_song:str = None):
        """
        This method allows you to change the value of the attribute song.
        """
        if (new_song is not None):
            self.song = fd.capital_first(str(new_song))
        else:
            raise Exception("No song was typed in the method set_artist(). Please type one and retry.")

    def set_lyric(self, new_lyric:str = None):
        """
        This method allows you to change the value of the attribute lyric.
        """
        if (new_lyric is not None):
            self.lyric = fd.capital_first(str(new_lyric))
        else:
            raise Exception("No song was typed in the method set_artist(). Please type one and retry.")

    def get_artist(self):
        """
        This method returns the value of the attribute artist.
        """
        return self.artist
    
    def get_song(self):
        """
        This method returns the value of the attribute song.
        """
        return self.song

    def get_lyric(self):
        """
        This method returns the value of the attribute lyric.
        """
        return self.lyric

    def download(self, chrome:str = None, debug = 'INFO'):
        """
        This method downloads from www.lyrics.com the lyric of the song and artist specified in the input object 
        instance_SongLyric of class SongLyric.

        Args:
            chrome: string - path of the chromedriver; if no path is passed, the application will try 
                                   to retrieve it from the PATH environment variable (default None)
            debugLevel: string - debug level; values:
                DEBUG          : Maximum level of debug, in addition to the same traces available for level INFO, 
                                 Chrome is started with graphical interface 
                INFO (default) : Chrome is started with no graphical interface
                WARNING        : Chrome is started with no graphical interface and only warning or more critical messages are displayed
            

        Output:
            self.lyric: string - it contains the lyric downloaded from www.lyrics.com
        """

        if (self.artist is not None and self.song is not None):
            
            self.lyric= fd.download_song(self.get_artist(), self.get_song(), chrome = chrome, debugLevel = debug)

        else:
            raise Exception("Cannot download the lyric: either artist or song (or both) are None, while both must be valued.")

    def translate(self, target_lang:str = "it"):
        """
        This method uses AWS translation service to translate a lyric in the desired target language.
        This method can be used only if the attribute lyric of the object SongLyric is not empty.
        All lyrics are assumed to be in english

        Args:
            target_lang: str - code for the language the lyric should be translated to.
                        Valid codes are for example:
                            - it for italian
                            - fr for french

                            For a full lists of this code, please visit https://docs.aws.amazon.com/translate/latest/dg/what-is.html#what-is-languages

        """
                
        if self.lyric is None :
            raise Exception("No lyric stored in the object. You can call translate only on objects that have a non-null lyric.")
        else:    
            self.lang = target_lang
            lyric = self.get_lyric() 

            self.translated_lyric = fd.translate_song(lyric,target_lang)


############ CLASS LibrarySong ############

class LibrarySong():
    """
    This class allows to store a collection of SongLyric objects, allowing to 
    perform operations on them in an iterative way.

    Attributes:
        - list_song: list - list of objects of the class SongLyric
    """
    def __init__(self):

        self.list_song_lyric = list()

##################### METHODS #####################

    def add_song(self, instance_song_lyric: SongLyric):
        """
        This method append an object of the class SongLyric to the list of objects stored in 
        the attribute list_song_lyric
        """
        self.list_song_lyric.append(instance_song_lyric)

    def __iter__(self):
        """
        This method returns an object of the iterator class IteratorLybrary thanks to which 
        the class LibrarySong becomes Iterable

        Example:
        testSong = ldc.SongLyric(artist = "timberlake Justin", song = "cry me a river", lyric = "test lyric1")
        testSong2 = ldc.SongLyric(artist = "dire straits", song = "sultans of swing", lyric = "test lyric2")
        library_song = ldc.LibrarySong()
        library_song.add_song(testSong)
        library_song.add_song(testSong2)

        # "for" cycle over the elements of library_song which in this example is a list of 2 objects: testSong and testSong2
        for song in library_song:

		    print(song[1]) # returns the name of the artist 
		    print(song[2]) # returns the name of the song
		    print(song[3]) # returns the lyrics

        """
        return IteratorLybrary(self)

    def retrieve_by_song(self, song_name:str, returned_values:int = 3):
        """
        This method returns the list of SongLyric objects corresponding to the song specified in the input parameter song_name

        Args:
            song_name: str - name of the song to search in the Library
            returned_values: int - Depending on its value the sublists of matching_position output variable will have                               different info - see also Output variables
                                    Specifically:
                                        - 3 (default) - return a list having position, Artist name, Song Name
                                        - 4 - like 3 plus the lyric
                                        - 5 - like 4 plus the translated lyric
        
        Output:
            matches: list - list that has as many elements as the ones that matches the song name;
                                    Each element of the list is a sublist made of the following elements (depending on the value of the input variable returned_values):
                                    - Position of the song in the list_song_lyric list
                                    - Artist Name
                                    - Song Name
                                    - Lyric
                                    - Language in which is translated
                                    - Translated lyric
        """
        song_name = fd.capital_first(str(song_name))

        matches = [[position,x[1:returned_values]] for position, x in enumerate(self) if x[2] == song_name] 

        return matches


    def retrieve_by_artist(self, artist_name:str, returned_values:int = 3):
        """
        This method returns the list of songs corresponding to the artist specified in the input parameter song_name.

        Args:
            artist_name: str - name of the artist to search in the Library
            returned_values: int - Depending on its value the sublists of matching_position output variable will have                               different info - see also Output variables
                                    Specifically:
                                        - 3 (default) - return a list having position, Artist name, Song Name
                                        - 4 - like 3 plus the lyric
                                        - 5 - like 4 plus the translated lyric
        
        Output:
            matches: list - list that has as many elements as the ones that matches the artist name;
                                    Each element of the list is a sublist made of the following elements:
                                    - Position of the song in the list_song_lyric list
                                    - Artist Name
                                    - Song Name
                                    - Lyric
                                    - Language in which is translated
                                    - Translated lyric
        """
        artist_name = fd.capital_first(str(artist_name))

        matches = [[position,x[1:returned_values]] for position, x in enumerate(self) if x[1] == artist_name] 

        return matches


    def retrieve_by_artist_and_song(self, artist_name:str, song_name:str, returned_values:int = 3):
        """
        This method returns the list of SongLyric objects corresponding to the song specified in the input parameter song_name

        Args
            artist_name: str - name of the artist to search in the Library
            song_name: str - name of the artist to search in the Library
            returned_values: int - Depending on its value the sublists of matching_position output variable will have                               different info - see also Output variables
                                    Specifically:
                                        - 3 (default) - return a list having position, Artist name, Song Name
                                        - 4 - like 3 plus the lyric
                                        - 5 - like 4 plus the translated lyric
        
        Output
            matches: list - list that has as many elements as the ones that matches the artist name;
                                    Each element of the list is a sublist made of the following elements:
                                    - Position of the song in the list_song_lyric list
                                    - Artist Name
                                    - Song Name
                                    - Lyric
                                    - Language in which is translated
                                    - Translated lyric
        """
        song_name = fd.capital_first(str(song_name))
        artist_name = fd.capital_first(str(artist_name))

        matches = [[position,x[1:returned_values]] for position, x in enumerate(self) if (x[1] == artist_name and x[2] == song_name ) ] 

        return matches


    def retrieve_song_by_index(self, song_position):

        return self.list_song_lyric[song_position]


############ CLASS IteratorLybrary ############

class IteratorLybrary():
    """
    This class constructs an iterator for the class LibrarySong

    Attributes:
        - iterable_library: list - list of objects of the class SongLyric
        - self.index: integer - index that keeps track of the iteration
    """
    def __init__(self, instance_library: LibrarySong):
        self.iterable_library = instance_library
        self.index = 0

##################### METHODS #####################

    def __next__(self):
        """Returns the next value from team object's lists"""
        if self.index < len(self.iterable_library.list_song_lyric):
            result = [None] * 6 # this can be improved ? maybe using something like list(len(self.iterable_library.__dict__))

            result[0] = self.iterable_library.list_song_lyric[self.index]
            result[1] = self.iterable_library.list_song_lyric[self.index].artist
            result[2] = self.iterable_library.list_song_lyric[self.index].song
            result[3] = self.iterable_library.list_song_lyric[self.index].lyric
            result[4] = self.iterable_library.list_song_lyric[self.index].translated_lyric
            result[5] = self.iterable_library.list_song_lyric[self.index].lang

            self.index += 1

            return result

        raise StopIteration  
        





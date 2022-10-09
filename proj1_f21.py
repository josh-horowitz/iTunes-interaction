#########################################
##### Name: Josh Horowitz           #####
##### Uniqname: joshor              #####
#########################################

import webbrowser
import requests

class Media:
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):
        self.json = json
        if self.json:
            if self.json.get('trackName'):
                self.title = self.json['trackName']
            elif self.json.get('collectionName'):
                self.title = self.json['collectionName']
            else:
                self.title = title
            if self.json.get('artistName'):
                self.author = self.json['artistName']
            else:
                self.author = author
            if self.json.get('releaseDate'):
                self.release_year = self.json['releaseDate'].split('-')[0]
            else:
                self.release_year = release_year
            if self.json.get('collectionViewUrl'):
                self.url = self.json['collectionViewUrl']
            else:
                self.url = url
        else:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url

# Other classes, functions, etc. should go here
    def info(self):
        return f"{self.title} by {self.author} ({self.release_year})"

    def length(self):
        return 0

class Song(Media):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", album="No Album", genre="No Genre", track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if self.json:
            if json.get('collectionName'):
                self.album = json['collectionName']
            else:
                self.album = album
            if json.get('primaryGenreName'):
                self.genre = json['primaryGenreName']
            else:
                self.genre = genre
            if json.get('trackTimeMillis'):
                self.track_length = json['trackTimeMillis']
            else:
                self.track_length = track_length
        else:
            self.album = album
            self.genre = genre
            self.track_length = track_length

    def info(self):
        return super().info() + f" [{self.genre}]"

    def length(self):
        return round(self.track_length/1000)

class Movie(Media):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating="No Rating", movie_length=0, json=None):
        super().__init__(title, author, release_year, url, json)

        if self.json:
            if json.get('contentAdvisoryRating'):
                self.rating = json['contentAdvisoryRating']
            else:
                self.rating = rating
            if json.get('trackTimeMillis'):
                self.movie_length = json['trackTimeMillis']
            else:
                self.movie_length = movie_length
        else:
            self.rating = rating
            self.movie_length = movie_length

    def info(self):
        return super().info() + f" [{self.rating}]"

    def length(self):
        return round((self.movie_length/1000)/60)

def getiTunesData(keys=None):
    parameterString = 'https://itunes.apple.com/search'

    response = requests.get(parameterString, params=keys)
    return createObjectsFromJSON(response.json()['results'])

def createObjectsFromJSON(jsonData):
    objectList = []

    for item in jsonData:
        if item.get('kind') == 'feature-movie':
            objectList.append((Movie(json=item), 'Movie'))
        elif item.get('kind') == 'song':
            objectList.append((Song(json=item), 'Song'))
        else:
            objectList.append((Media(json=item), 'Media'))

    return objectList

def searchStart(previousResults=None):
    if not previousResults:
        searchCriteria = input("Enter a search term or \"exit\" to quit: ")
    else:
        searchCriteria = input("Enter a number for more info, or another search term, or \"exit\" to quit: ")
    if searchCriteria.lower() != "exit":
        try:
            number = int(searchCriteria)
            outboundURL = previousResults[number-1].url
            print(f"Launching {outboundURL} in web browser.")
            webbrowser.open(outboundURL)
            return searchStart(previousResults)
        except:
            try:
                results = getiTunesData({'term': searchCriteria.strip().replace(' ', '+')})
                if results:
                    return results
                else:
                    print('No results found. Please try again')
                    searchStart()
            except:
                print("There was an issue with your entry. Please try again")
                searchStart()
    else:
        print('Thanks for using iTunes Search!')

def printResults(searchResults):
    songs = [song[0] for song in searchResults if song[1] == 'Song']
    movies = [movie[0] for movie in searchResults if movie[1] == 'Movie']
    medias = [media[0] for media in searchResults if media[1] == 'Media']

    count = 1
    print('SONGS')
    for song in songs:
        print(f"{count} {song.info()}")
        count += 1

    print('MOVIES')
    for movie in movies:
        print(f"{count} {movie.info()}")
        count += 1

    print('OTHER MEDIA')
    for media in medias:
        print(f"{count} {media.info()}")
        count += 1

    return songs + movies + medias

if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here

    userInput = searchStart()

    while userInput:
        previousResults = printResults(userInput)
        userInput = searchStart(previousResults)

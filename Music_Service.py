import datetime

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.playlists = []
        self.liked_tracks = []
        self.fav_artists = []
        self.history = History(self)

    def __str__(self):
        return f"{self.username}"

        
class Artist:
    def __init__(self, username, bio):
        self.username = username
        self.bio = bio

    def __str__(self):
        return self.username

class Album:
    def __init__(self, tracks: list, title, year, author):
        self.tracks = tracks
        self.title = title
        self.year = year
        self.author = author

    def __str__(self):
        return f"{self.title} - {self.author} [{self.year}]"

        
class Track:
    def __init__(self, title, duration, author, genre, rating = None):
        self.title = title
        self.duration = duration
        self.author = author
        self.genre = genre
        self.rating = rating

    def __str__(self):
        
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{self.author} — {self.title} [{minutes}:{seconds:02d}]"


class Playlist:
    def __init__(self, tracks, title, author, is_public):
        self.tracks = tracks
        self.title = title
        self.author = author
        self.is_public = is_public

    def __str__(self):
        return f"{self.title} - {self.author}"

    
class Genre:
    def __init__(self, type_genre):
        self.type_genre = type_genre

    def __str__(self):
        return self.type_genre



class History:
    def __init__(self, user):
        self.user = user
        self.listened_track = []
        self.last_track = []


class Rating:
    def __init___(self, user, track, value):
        self.user = user
        self.track = track
        self.value = value


class Lyrics:
    def __init__(self, text, track):
        self.text = text
        self.track = track


class Download:
    def __init__(self, user, track):
        self.user = user
        self.track = track
        self.date = datetime.now()
    
    def __str__(self):
        return f"{self.track} скачен {self.user}"


if __name__ == "__main__":
    ...

        

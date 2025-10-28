import uuid

class Generator_ID:
    def get_id():
        pass


class AutoID(Generator_ID):
    def get_id():
        return uuid.uuid4().hex[:8]

class Device:
    def __init__(self, name: str, os: str):
        self.id = AutoID.get_id()
        self.name = name
        self.os = os

    def __str__(self):
        return f"{self.name} - {self.os}[{self.id}]"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "os": self.os
        }


class User:
    def __init__(self, username: str, email: str, device: Device = Device("PC", 'Windows')):
        self.id = AutoID.get_id()
        self.username = username
        self.email = email
        self.device = device

    def __str__(self):
        return f"{self.username}[{self.id}]"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "device_id": self.device.id
        }


class Tag:
    def __init__(self, name: str, track: 'Track'):
        self.id = AutoID.get_id()
        self.name = name
        self.track_id = track.id

    def __str__(self):
        return f"{self.name} - {self.track_id}"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "track_id" : self.track_id}


class Artist:
    def __init__(self, username: str, bio: str):
        self.id = AutoID.get_id()
        self.username = username
        self.bio = bio

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio
        }


class Track:
    def __init__(self, title: str, duration: int, artist: Artist):
        self.id = AutoID.get_id()
        self.title = title
        self.duration = duration
        self.artist = artist

    def __str__(self):
        minute = self.duration // 60
        seconds = self.duration % 60
        return f"{self.title} - {minute}:{seconds}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "duration": self.duration,
            "artist_id": self.artist.id
        }


class Album:
    def __init__(self, tracks: list['Track'], title: str, year: int, artist: Artist):
        self.id = AutoID.get_id()
        self.tracks = tracks
        self.title = title
        self.year = year
        self.artist = artist

    def add_tracks(self, *tracks):
        for track in tracks:
            self.tracks.append(track)

    def del_tracks(self, *tracks):
        for track in tracks:
            self.tracks.remove(track)

    def show_tracks(self):
        for track in self.tracks:
            print(track)

    def to_dict(self):
        return {
            "id": self.id,
            "artist_id": self.artist.id,
            "title": self.title,
            "year": self.year,
            "track_ids": [track.id for track in self.tracks]
        }
    

class Lyrics:
    def __init__(self, text: str, track: Track):
        self.id = AutoID.get_id()
        self.text = text
        self.track = track

    def __str__(self):
        return f"{self.track} - {self.text}"

    def to_dict(self):
        return {
            "id": self.id,
            "track_id": self.track.id,
            "lyrics": self.text
        }

        
      
class Genre:
    def __init__(self, type_genre: str, track: Track):
        self.id = AutoID.get_id()
        self.type_genre = type_genre
        self.track = track

    def __str__(self):
        return f"{self.type_genre} - {self.track}"

    def to_dict(self):
        return {
            "id": self.id,
            "type_genre": self.type_genre,
            "track_id": self.track.id
        }


class Playlist:
    def __init__(self, tracks: list['Track'], title: str, author: User, is_public=True):
        self.id = AutoID.get_id()
        self.tracks = tracks
        self.title = title
        self.is_public = is_public
        self.author = author

    def add_tracks(self, *tracks):
        for track in tracks:
            self.tracks.append(track)
            print('Добавлено')

    def del_tracks(self, *tracks):
        for track in tracks:
            self.tracks.remove(track)

    def show_tracks(self):
        for track in self.tracks:
            print(track)

    def to_dict(self):
        return {
            "id": self.id,
            "author_id": self.author.id,
            "title": self.title,
            "is_public": self.is_public,
            "track_ids": [track.id for track in self.tracks]
        }
    

class Queue:
    def __init__(self, user: User, tracks: list['Track']):
        self.id = AutoID.get_id()
        self.user = user
        self.tracks = tracks

    def add_to_queue(self, *tracks: 'Track'):
        for track in tracks:
            self.tracks.append(track)

    def next_track(self):
        if self.tracks:
            return self.tracks.pop(0)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "track_ids": [t.id for t in self.tracks]
        }

if __name__ == "__main__":
    pass
        

        

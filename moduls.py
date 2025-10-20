import datetime
import json
import uuid

class AutoID:
    def get_id():
        return uuid.uuid4().hex[:8]

class Device:
    def __init__(self, name: str, os: str):
        self.id = AutoID.get_id()
        self.name = name
        self.os = os

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "os": self.os
        }


class User:
    def __init__(self, username: str, email: str, device: Device):
        self.id = AutoID.get_id()
        self.username = username
        self.email = email
        self.device = device

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "device_id": self.device.id
        }


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

    def to_dict(self):
        return {
            "id": self.id,
            "author_id": self.author.id,
            "title": self.title,
            "is_public": self.is_public,
            "track_ids": [track.id for track in self.tracks]
        }

if __name__ == "__main__":
    pass
        

        

import datetime
import json


class Device:
    def __init__(self, name: str, os: str):
        self.name = name
        self.os = os

    def set_device(self, name: str, os: str):
        self.name = name
        self.os = os

    def to_dict(self):
        return {"name": self.name,
                "os" : self.os}


class Album:
    def __init__(self, tracks: list['Track'], title: str, year: int):
        self.tracks = tracks
        self.title = title
        self.year = year

    def add_track(self, *tracks: list['Track']):
        for track in tracks:
            self.tracks.append(track)
        
    def adel_track(self, *tracks: list['Track']):
        for track in tracks:
            self.tracks.remove(track)


    def to_dict(self):
        return {
            "title": self.title,
            "year": self.year,
            "tracks": [track.title for track in self.tracks]
        }


class Rating:
    def __init__(self, value: int):
        self.value = value

    def to_dict(self):
        return {
            "value": self.value
        }
    

class Lyrics:
    def __init__(self, text: str):
        self.text = text

    def to_dict(self):
        return {"lyrics" : self.text}
        
      
class Genre:
    def __init__(self, type_genre: str):
        self.type_genre = type_genre

    def to_dict(self):
        return {"type_genre": self.type_genre}


class Track:
    def __init__(self, title: str, duration: int, rating: Rating, genre = Genre("Жанр не указан"), lyrics = Lyrics("Субтитры не указаны")):
        self.title = title
        self.duration = duration
        self.lyrics = lyrics
        self.genre = genre
        self.rating = rating
        

    def to_dict(self):
        return {
            "title": self.title,
            "duration": self.duration,
            "lyrics" : self.lyrics.to_dict(),
            "genre" : self.genre.to_dict(),
            "rating" : self.rating.to_dict()
        }


class Playlist:
    def __init__(self, tracks: list['Track'], title: str, is_public = True):
        self.tracks = tracks
        self.title = title
        self.is_public = is_public

    def show_tracks(self):
        return [track for track in self.tracks]
        
    def set_visibility(self, visibility: bool):
        self.is_public = visibility

    def add_tracks(self, *tracks: list['Track']):
        for track in tracks:
            self.tracks.append(track)

    def delete_tracks(self, *tracks: list['Track']):
        for track in tracks:
            self.tracks.remove(track)

    def to_dict(self):
        return {
            "title": self.title,
            "is_public": self.is_public,
            "tracks": [track.to_dict() for track in self.tracks]
        }


class User:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        self.playlists = []
        self.liked_tracks = []
        self.fav_artists = []
        self.device = Device(name="PC", os="Windows 11")

    def to_dict(self):
        return {
            "username" : self.username,
            "email" : self.email,
            "playlists" : [playlist.to_dict() for playlist in self.playlists if self.playlists],
            "liked_tracks" : [track.to_dict() for track in self.liked_tracks if self.liked_tracks],
            "fav_artists" : [{"username" : art.username, "bio" : art.bio} for art in self.fav_artists if self.fav_artists],
            "device" : self.device.to_dict()
        }
        
    def like_track(self, *tracks: list['Track']):
        for track in tracks:
            self.liked_tracks.append(track)

    def delete_track(self, *tracks: list['Track']):
        for track in tracks:
            self.liked_tracks.remove(track)

    def list_of_fav_track(self):
        return [track for track in self.liked_tracks if self.liked_tracks]
    
    def add_playlists(self, *playlists: list["Playlist"]):
        for playlist in playlists:
            self.playlists.append(playlist)

    def delete_playlists(self, *playlists: list["Playlist"]):
        for playlist in playlists:
            self.playlists.remove(playlist)

    def list_of_playlists(self):
        return [playlist for playlist in self.playlists]

    def add_fav_artisits(self, *artists: list['Artist']):
        for art in artists:
            self.fav_artists.append(art)

    def del_fav_artisits(self, *artists: list['Artist']):
        for art in artists:
            self.fav_artists.remove(art)

    def show_fav_artists(self):
        return [art for art in self.fav_artists]
    
        
class Artist:
    def __init__(self, username: str, bio: str):
        self.username = username
        self.bio = bio
        self.albums = []
        self.tracks = []
        
    def to_dict(self):
        return {
            "username": self.username,
            "bio": self.bio,
            "albums" : [album.to_dict() for album in self.albums if self.albums],
            "tracks" : [track.to_dict() for track in self.tracks if self.tracks],
        }


class Service:
    def __init__(self, user = None, artist = None):
        self.users = [user]
        self.artists = [artist]
        
    def to_json(self, filename):
        try:
            data = {"music_service" : {"users" : [user.to_dict() for user in self.users if user is not None],
                    "artists" : [artist.to_dict() for artist in self.artists if artist is not None]}}
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Данные успешно сохранены в {filename}")
        
        except Exception as e:
            print(f"Ошибка при сохранении в JSON: {e}")
        

if __name__ == "__main__":
    ...

        

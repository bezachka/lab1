from moduls import User, Artist, Track, Playlist, Album, AutoID, Device, Lyrics, Genre
import json

class Service:
    def __init__(self, users=None, artists=None, tracks=None, albums=None, playlists=None, lyrics=None, genres=None):
        self.users = users or []
        self.artists = artists or []
        self.tracks = tracks or []
        self.albums = albums or []
        self.playlists = playlists or []
        self.lyrics = lyrics or []
        self.genres = genres or []


class ServiceSerializer:

    def to_json(service: Service, filename: str):
        try:
            data = {
                "music_service": {
                    "users": [user.to_dict() for user in service.users],
                    "artists": [artist.to_dict() for artist in service.artists],
                    "tracks": [track.to_dict() for track in service.tracks],
                    "albums": [album.to_dict() for album in service.albums],
                    "playlists": [playlist.to_dict() for playlist in service.playlists],
                    "lyrics": [lyric.to_dict() for lyric in service.lyrics],
                    "genres": [genre.to_dict() for genre in service.genres]
                }
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"Данные успешно сохранены в {filename}")

        except Exception as e:
            print(f"Ошибка при сохранении в JSON: {e}")


   
    def from_json(filename: str) -> Service:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            data = data.get("music_service", {})

            # ===== Artists =====
            artists = []
            artist_map = {}
            for a in data.get("artists", []):
                artist = Artist(username=a.get("username", ""), bio=a.get("bio", ""))
                artist.id = a.get("id")
                artists.append(artist)
                artist_map[artist.id] = artist

            # ===== Tracks =====
            tracks = []
            track_map = {}
            for t in data.get("tracks", []):
                artist_id = t.get("artist_id")
                artist = artist_map.get(artist_id)
                track = Track(
                    title=t.get("title", ""),
                    duration=t.get("duration", 0),
                    artist=artist
                )
                track.id = t.get("id")
                tracks.append(track)
                track_map[track.id] = track

            # ===== Users =====
            users = []
            user_map = {}
            for u in data.get("users", []):
                device = Device(name=u.get("device_id", ""), os="")
                user = User(
                    username=u.get("username", ""),
                    email=u.get("email", ""),
                    device=device
                )
                user.id = u.get("id")
                users.append(user)
                user_map[user.id] = user

            # ===== Albums =====
            albums = []
            album_map = {}
            for a in data.get("albums", []):
                artist_id = a.get("artist_id")
                artist = artist_map.get(artist_id)
                album_tracks = [track_map.get(tid) for tid in a.get("track_ids", []) if tid in track_map]

                album = Album(
                    tracks=album_tracks,
                    title=a.get("title", ""),
                    year=a.get("year", 0),
                    artist=artist
                )
                album.id = a.get("id")
                albums.append(album)
                album_map[album.id] = album

            # ===== Playlists =====
            playlists = []
            for p in data.get("playlists", []):
                author_id = p.get("author_id")
                author = user_map.get(author_id)

                playlist_tracks = [
                    track_map.get(tid) for tid in p.get("track_ids", [])
                    if tid in track_map
                ]

                playlist = Playlist(
                    tracks=playlist_tracks,
                    title=p.get("title", ""),
                    author=author,
                    is_public=p.get("is_public", True)
                )
                playlist.id = p.get("id")
                playlists.append(playlist)

            # ===== Lyrics =====
            lyrics = []
            for l in data.get("lyrics", []):
                track = track_map.get(l.get("track_id"))
                lyric = Lyrics(text=l.get("lyrics", ""), track=track)
                lyric.id = l.get("id")
                lyrics.append(lyric)

            # ===== Genres =====
            genres = []
            for g in data.get("genres", []):
                track = track_map.get(g.get("track_id"))
                genre = Genre(type_genre=g.get("type_genre", ""), track=track)
                genre.id = g.get("id")
                genres.append(genre)

            return Service(
                users=users,
                artists=artists,
                tracks=tracks,
                albums=albums,
                playlists=playlists,
                lyrics=lyrics,
                genres=genres
            )

        except Exception as e:
            print(f"❌ Ошибка при чтении JSON: {e}")
            return None



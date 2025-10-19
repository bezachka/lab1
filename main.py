from Music_Service import Artist, Genre, Track, User, Playlist, Service, Album, Rating

author1 = Artist("Artist1", "bio1")
author2 = Artist("Artist2", "bio2")

genre1 = Genre("Рок")

track1 = Track("Track1", 134, rating=Rating(5))
track2 = Track("Track2", 72, rating=Rating(5))
track3 = Track("Track3", 102, rating=Rating(5))
track4 = Track("Track4", 252,  rating=Rating(5))

user1 = User("beza", "lol@gmail.com")


playlist1 = Playlist([track1, track2, track3, track4], "playlist1", is_public=True)
user1.add_playlists(playlist1)
user1.like_track(Track("Track5", 230, Rating(4)))
user1.add_fav_artisits(Artist("Artist3", "bio3"))

structure = Service(user = user1, artist= author1)
structure.to_json("music_structure_1.json")

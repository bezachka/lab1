from Music_Service import Artist, Genre, Track, User, Playlist

author1 = Artist("Серега Пират", "Стример по Доте 2 и Артист")

genre1 = Genre("Рок")

track1 = Track("Я это я", 134, author1, genre1)
track2 = Track("В этой траве", 72, author1, genre1)

user1 = User("beza", "lol@gmail.com")

playlist1 = Playlist([track1, track2], "Имба", author1, True)
user1.add_playlists(playlist1)
user1.list_of_playlists()
playlist1.lst_trk()

user1.list_of_fav_track()
user1.like_track(track2, track1)
user1.list_of_fav_track()

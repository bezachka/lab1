from moduls import User, Artist, Track, Playlist, Album, AutoID, Device, Lyrics, Genre, Tag, Queue
import json
from lxml import etree
import os

class Service:
    def __init__(self, users=None, artists=None, tracks=None, albums=None, playlists=None, lyrics=None, genres=None, devices = None, tags = None, queues = None):
        self.users = users or []
        self.artists = artists or []
        self.tracks = tracks or []
        self.albums = albums or []
        self.playlists = playlists or []
        self.lyrics = lyrics or []
        self.genres = genres or []
        self.devices = devices or []
        self.tags = tags or []
        self.queues = queues or []


class JsonServiceSerializer:

    def to_json(service: Service, filename: str):
        try:
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                exist_data = {"music_service": {}}
            else:
                with open(filename, 'r', encoding='utf-8') as f:
                    exist_data = json.load(f)

            if "music_service" not in exist_data:
                exist_data["music_service"] = {}

            # Новые данные
            data = {
                "users": [u.to_dict() for u in service.users],
                "artists": [a.to_dict() for a in service.artists],
                "tracks": [t.to_dict() for t in service.tracks],
                "albums": [a.to_dict() for a in service.albums],
                "playlists": [p.to_dict() for p in service.playlists],
                "lyrics": [l.to_dict() for l in service.lyrics],
                "genres": [g.to_dict() for g in service.genres],
                "devices": [d.to_dict() for d in service.devices],
                "tags": [t.to_dict() for t in service.tags],
                "queues": [q.to_dict() for q in service.queues],
            }

            # Обновляем или добавляем
            for key, value_list in data.items():
                if key not in exist_data["music_service"]:
                    exist_data["music_service"][key] = []

                # обновляем или добавляем объекты
                existing_list = exist_data["music_service"][key]

                for item in value_list:
                    found = False
                    for i, existing_obj in enumerate(existing_list):
                        if existing_obj.get("id") == item["id"]:
                            # заменяем старую версию новым объектом (обновляем связи и поля)
                            existing_list[i] = item
                            found = True
                            print(f"🔁 Обновлён объект с id={item['id']} в {key}")
                            break
                    if not found:
                        existing_list.append(item)
                        print(f"➕ Добавлен новый объект в {key} (id={item['id']})")


            # Сохраняем JSON
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(exist_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Данные успешно сохранены в {filename}")

        except Exception as e:
            print(f"❌ Ошибка при сохранении JSON: {e}")

    def from_json(filename: str) -> Service:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            data = data.get("music_service", {})

            devices = []
            devices_map = {}
            for a in data.get("devices", []):
                device = Device(name=a.get("name", ""), os=a.get("os", ""))
                device.id = a.get("id")
                devices.append(device)
                devices_map[device.id] = device

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
                device_ids = u.get("device_id", [])
                if isinstance(device_ids, list) and device_ids:
                    device = devices_map.get(device_ids[0])  # берём первое устройство
                elif isinstance(device_ids, str):
                    device = devices_map.get(device_ids)
                else:
                    device = None

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

            tags = []
            for g in data.get("tags", []):
                track = track_map.get(g.get("track_id"))
                tag = Tag(name=g.get("name", ""), track=track)
                tag.id = g.get("id")
                tags.append(tag)

            queues = []
            for p in data.get("queues", []):
                user_id = p.get("user_id")
                user = user_map.get(user_id)

                queue_tracks = [
                    track_map.get(tid) for tid in p.get("track_ids", [])
                    if tid in track_map
                ]

                queue = Queue(
                    tracks=queue_tracks,
                    user = user
                )
                queue.id = p.get("id")
                queues.append(queue)

            return Service(
                users=users,
                artists=artists,
                tracks=tracks,
                albums=albums,
                playlists=playlists,
                lyrics=lyrics,
                genres=genres,
                devices = devices,
                tags = tags,
                queues= queues

            )

        except Exception as e:
            print(f"❌ Ошибка при чтении JSON: {e}")
            return None




class LxmlServiceSerializer:
    def to_lxml(service: Service, filename: str):
        try:
            # Проверяем, существует ли файл
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                tree = etree.parse(filename)
                root = tree.getroot()
            else:
                root = etree.Element("MusicService")
                tree = etree.ElementTree(root)

            # Словарь существующих секций
            existing_sections = {child.tag: child for child in root}

            # Категории для сохранения
            categories = [
                ("users", service.users), ("artists", service.artists),
                ("tracks", service.tracks), ("albums", service.albums),
                ("playlists", service.playlists), ("genres", service.genres),
                ("lyrics", service.lyrics), ("devices", service.devices),
                ("tags", service.tags), ("queues", service.queues),
            ]

            for category, items in categories:
                # создаем раздел, если его нет
                if category not in existing_sections:
                    category_elem = etree.SubElement(root, category)
                    existing_sections[category] = category_elem
                else:
                    category_elem = existing_sections[category]

                # --- собираем все существующие элементы в словарь id -> элемент ---
                existing_elems = {}
                for elem in category_elem.findall(category[:-1]):
                    id_elem = elem.find("id")
                    if id_elem is not None and id_elem.text:
                        existing_elems[id_elem.text] = elem

                # --- добавляем или обновляем объекты ---
                for item in items:
                    item_dict = item.to_dict()
                    item_id = str(item.id)

                    # если элемент с таким id уже есть → обновляем его
                    if item_id in existing_elems:
                        old_elem = existing_elems[item_id]
                        category_elem.remove(old_elem)
                        print(f"🔁 Обновлён объект {category[:-1]} с id={item_id}")

                    else:
                        print(f"➕ Добавлен новый объект {category[:-1]} с id={item_id}")

                    # создаем новый элемент
                    item_elem = etree.SubElement(category_elem, category[:-1])

                    # записываем обычные поля
                    for key, value in item_dict.items():
                        if key not in ['track_ids', 'author_id', 'device_id', 'artist_id', 'user_id']:
                            elem = etree.SubElement(item_elem, key)
                            elem.text = str(value)

                    # связи (устройства, автор, артист, треки)
                    if hasattr(item, 'device') and item.device:
                        if isinstance(item.device, list):
                            devices_elem = etree.SubElement(item_elem, "device_ids")
                            for dev in item.device:
                                etree.SubElement(devices_elem, "device_id").text = str(dev.id)
                        else:
                            etree.SubElement(item_elem, "device_id").text = str(item.device.id)

                    if hasattr(item, 'artist') and item.artist:
                        etree.SubElement(item_elem, "artist_id").text = str(item.artist.id)

                    if hasattr(item, 'author') and item.author:
                        etree.SubElement(item_elem, "author_id").text = str(item.author.id)

                    if hasattr(item, 'user') and item.user:
                        etree.SubElement(item_elem, "user_id").text = str(item.user.id)

                    if hasattr(item, 'tracks') and item.tracks:
                        tracks_elem = etree.SubElement(item_elem, "track_ids")
                        for track in item.tracks:
                            etree.SubElement(tracks_elem, "track_id").text = str(track.id)

            # Сохраняем XML
            tree.write(filename, pretty_print=True, xml_declaration=True, encoding='utf-8')
            print(f"✅ Данные успешно добавлены/обновлены в {filename}")

        except Exception as e:
            print(f"Ошибка при сохранении в XML: {e}")


    

    def from_lxml(filename: str) -> Service:
        try:
            tree = etree.parse(filename)
            root = tree.getroot()
            
            # Создаем карты для связей
            artist_map = {}
            track_map = {}
            device_map = {}
            user_map = {}
            
            # Парсим все категории
            data = {}
            for category in ["artists", "tracks", "users", "albums", "playlists", "genres", "lyrics", "devices", "tags", "queues"]:
                data[category] = []
                for item_elem in root.findall(f".//{category}/{category[:-1]}"):
                    item_data = {}
                    for child in item_elem:
                        if child.tag == "track_ids":
                            item_data[child.tag] = [elem.text for elem in child]
                        else:
                            item_data[child.tag] = child.text
                    data[category].append(item_data)
            
            # ===== Devices =====
            devices = []
            for d_data in data["devices"]:
                device = Device(name=d_data.get("name", ""), os=d_data.get("os", ""))
                device.id = d_data.get("id", "")
                devices.append(device)
                device_map[device.id] = device
            
            # ===== Artists =====
            artists = []
            for a_data in data["artists"]:
                artist = Artist(username=a_data.get("username", ""), bio=a_data.get("bio", ""))
                artist.id = a_data.get("id", "")
                artists.append(artist)
                artist_map[artist.id] = artist
            
            # ===== Tracks =====
            tracks = []
            for t_data in data["tracks"]:
                artist = artist_map.get(t_data.get("artist_id"))
                track = Track(title=t_data.get("title", ""), duration=int(t_data.get("duration", 0)), artist=artist)
                track.id = t_data.get("id", "")
                tracks.append(track)
                track_map[track.id] = track
            
            # ===== Users =====
            users = []
            for u_data in data["users"]:
                device = device_map.get(u_data.get("device_id"))  # только одно устройство
                user = User(
                    username=u_data.get("username", ""),
                    email=u_data.get("email", ""),
                    device=device
                )
                user.id = u_data.get("id", "")
                users.append(user)
                user_map[user.id] = user
            
            # ===== Albums =====
            albums = []
            for a_data in data["albums"]:
                artist = artist_map.get(a_data.get("artist_id"))
                album_tracks = [track_map[tid] for tid in a_data.get("track_ids", []) if tid in track_map]
                album = Album(tracks=album_tracks, title=a_data.get("title", ""), year=int(a_data.get("year", 0)), artist=artist)
                album.id = a_data.get("id", "")
                albums.append(album)
            
            # ===== Playlists =====
            playlists = []
            for p_data in data["playlists"]:
                author = user_map.get(p_data.get("author_id"))
                playlist_tracks = [track_map[tid] for tid in p_data.get("track_ids", []) if tid in track_map]
                playlist = Playlist(tracks=playlist_tracks, title=p_data.get("title", ""), author=author, is_public=p_data.get("is_public", "true").lower() == "true")
                playlist.id = p_data.get("id", "")
                playlists.append(playlist)
            
            # ===== Lyrics =====
            lyrics = []
            for l_data in data["lyrics"]:
                track = track_map.get(l_data.get("track_id"))
                lyric = Lyrics(text=l_data.get("lyrics", ""), track=track)
                lyric.id = l_data.get("id", "")
                lyrics.append(lyric)
            
            # ===== Genres =====
            genres = []
            for g_data in data["genres"]:
                track = track_map.get(g_data.get("track_id"))
                genre = Genre(type_genre=g_data.get("type_genre", ""), track=track)
                genre.id = g_data.get("id", "")
                genres.append(genre)
            
            # ===== Tags =====
            tags = []
            for t_data in data["tags"]:
                track = track_map.get(t_data.get("track_id"))
                tag = Tag(name=t_data.get("name", ""), track=track)
                tag.id = t_data.get("id", "")
                tags.append(tag)
            
            # ===== Queues =====
            queues = []
            for q_data in data["queues"]:
                user = user_map.get(q_data.get("user_id"))
                queue_tracks = [track_map[tid] for tid in q_data.get("track_ids", []) if tid in track_map]
                queue = Queue(user=user, tracks=queue_tracks)
                queue.id = q_data.get("id", "")
                queues.append(queue)
            
            return Service(
                users=users, artists=artists, tracks=tracks, albums=albums,
                playlists=playlists, lyrics=lyrics, devices=devices, genres=genres, tags=tags, queues=queues
            )
    
        except Exception as e:
            print(f"Ошибка при чтении XML: {e}")
            return None

if __name__ == "__main__":
    # Создание артистов
    artist1 = Artist(username="Eminem", bio="Rapper")
    artist2 = Artist(username="LinkinPark", bio="Rock band")

    # Создание треков
    track1 = Track(title="Lose Yourself", duration=326, artist=artist1)
    track2 = Track(title="Numb", duration=210, artist=artist2)

    # Создание юзера и устройства
    device1 = Device(name="iPhone", os="iOS")
    user1 = User(username="john_doe", email="john@example.com", device=device1)

    # Создание альбома
    album1 = Album(tracks=[track1, track2], title="Best Hits", year=2020, artist=artist1)

    # Создание плейлиста
    playlist1 = Playlist(tracks=[track1], title="My Playlist", author=user1)

    # Создание текста песни и жанра
    lyrics1 = Lyrics(text="Look, if you had one shot...", track=track1)
    genre1 = Genre(type_genre="Rap", track=track1)

    # Формируем сервис
    service = Service(
        users=[user1],
    )

    # Сохранение

    JsonServiceSerializer.to_json(service, "music_service.json")

    loaded_service = JsonServiceSerializer.from_json("music_service.json")
    loaded_service_xml = LxmlServiceSerializer.from_lxml("music_test.xml")

    
    
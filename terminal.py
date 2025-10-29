from service import *
from moduls import *
from exceptions import TerminalException, FileProcessingError, UserInputError

class Terminal():
    def __init__(self):
        pass

    def load(filename, type_data):

        if type_data == "json":
            return JsonServiceSerializer.from_json(filename)
        elif type_data == "xml":
            return LxmlServiceSerializer.from_lxml(filename)
        else:
            raise FileProcessingError(f"Неизвестный тип данных: {type_data}")

        
    def save(filename, type_data, service: Service):

        if type_data == "json":
            JsonServiceSerializer.to_json(service, filename)
        elif type_data == "xml":
            LxmlServiceSerializer.to_lxml(service, filename)
        else:
            raise FileProcessingError(f"Неизвестный тип данных: {type_data}")

            
    def create_user():
            username = input("Имя пользователя: ")
            email = input("Email: ")
            if "@" not in email:
                raise UserInputError("Почта не валидная")
            dev_name = input("Имя устройства: ")
            dev_os = input("ОС: ")
            device = Device(dev_name, dev_os)
            user = User(username=username, email=email, device=device)

            return [user, device]
        



    def start_terminal():
        
        type_data = "json"
        filename = "music_service.json"
        
        while True:
            service = Terminal.load(filename, type_data)
            print(f"Текущий файл: {filename}")
            print(f"Тип данных: {type_data}")
            print(f"1. Пользователи\n2. Артисты\n3. Устройства\n4. Треки\n5. Плейлисты\n6. Альбомы\n7. Очереди\n8. Субтитры\n9. Жанры\n10. Тэги\n" \
            "11. Считать данные\n12. Выход из Терминала")

            try:
                choice = int(input("Выберите действие [1-12]: "))
            except ValueError:
                print("Введите число от 1 до 12")
                continue
            except Exception:
                print("Некорректный ввод")
                continue

            #Пользователи
            if choice == 1:
                if service.users:
                    print("\nПользователи:")
                    for i, user in enumerate(service.users, 1):
                        print(f"{i}. {user}")
                else:
                    print("Пользователей нет.")
                
                ans = input("\nСоздать нового пользователя? [да/нет]: ")
                if ans.lower() == "да":
                    try:
                        data_user = Terminal.create_user()
                    except Exception as e:
                        print(f"Произошла ошибка: {e}")
                        continue
                    Terminal.save(filename, type_data, Service(users=[data_user[0]], devices=[data_user[1]]))
                    print(f"Пользователь добавлен.")

            #Артисты
            elif choice == 2:
                if service.artists:
                    print("\nАртисты:")
                    for i, artist in enumerate(service.artists, 1):
                        print(f"{i}. {artist.username} — {artist.bio}")
                else:
                    print("Артистов нет.")
                ans = input("\nСоздать нового артиста? [да/нет]: ")
                if ans.lower() == "да":
                    name = input("Имя артиста: ")
                    bio = input("Биография: ")
                    Terminal.save(filename, type_data, Service(artists=[Artist(name, bio)]))
                    print(f"✅ Артист {name} добавлен.")

            #Устройства
            elif choice == 3:
                if service.devices:
                    print("\nУстройства:")
                    for i, d in enumerate(service.devices, 1):
                        print(f"{i}. {d.name} ({d.os}) [{d.id}]")
                else:
                    print("Устройств нет.")
                

            #Треки
            elif choice == 4:
                if service.tracks:
                    print("\nТреки:")
                    for i, t in enumerate(service.tracks, 1):
                        print(f"{i}. {t.title} — {t.artist.username}")
                else:
                    print("Пока треков нет")

                ans = input("\nСоздать новый трек? [да/нет]: ").strip().lower()
                if ans == "да":
                    title = input("Введите название трека: ").strip()
                    duration = int(input("Введите длительность (в секундах): "))

                    # Выбор артиста
                    artist = None
                    if service.artists:
                        print("\nДоступные артисты:")
                        for i, a in enumerate(service.artists, 1):
                            print(f"{i}. {a.username} — {a.bio}")

                        ans_art = input("\nВыберите артиста по номеру или введите 'новый' для создания нового: ").strip()

                        if ans_art.lower() == "новый":
                            artist_name = input("Имя нового артиста: ").strip()
                            artist_bio = input("Биография артиста: ").strip()
                            artist = Artist(username=artist_name, bio=artist_bio)
                            print(f"Создан новый артист: {artist.username}")
                        else:
                            try:
                                artist_index = int(ans_art) - 1
                                artist = service.artists[artist_index]
                                print(f"Выбран артист: {artist.username}")
                            except (IndexError, ValueError):
                                print("Неверный выбор артиста.")
                                continue
                    else:
                        print("\nАртистов пока нет — создаём нового")
                        artist_name = input("Имя артиста: ").strip()
                        artist_bio = input("Биография артиста: ").strip()
                        artist = Artist(username=artist_name, bio=artist_bio)

                    # Создаём трек
                    track = Track(title=title, duration=duration, artist=artist)

                    # Сохраняем всё
                    Terminal.save(filename, type_data, Service(tracks=[track], artists=[artist]))
                    print(f"Трек '{title}' успешно добавлен артисту {artist.username}.")


            #
            elif choice == 5:  # Плейлисты
                if service.playlists:
                    print("\nПлейлисты:\n")
                    for i, playlist in enumerate(service.playlists, 1):
                        print(f"{i}. {playlist.title} — Автор: {playlist.author.username}")
                else:
                    print("Плейлистов нет.")

                ans = input('\nВыберите действие: [1] Просмотреть плейлист, [2] Создать новый, [0] Назад: ').strip()

                #Просмотр плейлиста
                if ans == "1":
                    if not service.playlists:
                        print("Нет плейлистов для просмотра.")
                    else:
                        num = int(input("Введите номер плейлиста: ")) - 1
                        if 0 <= num < len(service.playlists):
                            playlist = service.playlists[num]
                            print(f"\nПлейлист: {playlist.title}")
                            print(f"Автор: {playlist.author.username}")
                            print(f"Публичный: {'Да' if playlist.is_public else 'Нет'}")

                            if playlist.tracks:
                                print("\nТреки в плейлисте:")
                                for i, track in enumerate(playlist.tracks, 1):
                                    print(f"{i}. {track}")
                            else:
                                print("Плейлист пуст.")

                            add_ans = input("\nДобавить трек в этот плейлист? [да/нет]: ").strip().lower()
                            if add_ans == "да":
                                if not service.tracks:
                                    print("Нет доступных треков.")
                                else:
                                    print("\n🎶 Доступные треки:")
                                    for i, t in enumerate(service.tracks, 1):
                                        print(f"{i}. {t.title} — {t.artist.username}")
                                    tnum = int(input("Выберите трек по номеру: ")) - 1
                                    if 0 <= tnum < len(service.tracks):
                                        playlist.tracks.append(service.tracks[tnum])
                                        Terminal.save(filename, type_data, Service(playlists=[playlist]))
                                        print(f"✅ Трек '{service.tracks[tnum].title}' добавлен в '{playlist.title}'")
                                    else:
                                        print("Неверный номер трека.")
                        else:
                            print("Неверный номер плейлиста.")

                #Создание нового плейлиста
                elif ans == "2":
                    title = input("Введите название плейлста: ").strip()
                    is_public = input("Публичный? [да/нет]: ").strip().lower() == "да"

                    #Выбираем автора
                    if service.users:
                        print("\nПользователи:")
                        for i, user in enumerate(service.users, 1):
                            print(f"{i}. {user.username}")
                        u_choice = int(input("Выберите автора по номеру: ")) - 1
                        author = service.users[u_choice]

                        playlist = Playlist(tracks=[], title=title, author=author, is_public=is_public)
                        Terminal.save(filename, type_data, Service(playlists=[playlist]))
                        print(f"✅ Плейлист '{title}' успешно создан пользователем {author.username}.")
                    else:
                        print("Нет пользователей, создадим нового:")
                        user_lst = Terminal.create_user()
                        # username = input("Имя пользователя: ")
                        # email = input("Email: ")
                        author = user_lst[0]

                        playlist = Playlist(tracks=[], title=title, author=author, is_public=is_public)
                        Terminal.save(filename, type_data, Service(playlists=[playlist], users=[user_lst[0]], devices=[user_lst[1]]))
                        print(f"✅ Плейлист '{title}' успешно создан пользователем {author.username}.")


            elif choice == 6:  #Альбомы
                if service.albums:
                    print("Альбомы:\n")
                    for i, album in enumerate(service.albums, 1):
                        print(f"{i}. {album.title} — {album.artist.username} ({album.year})")
                else:
                    print("Альбомов нет.")

                ans = input('\nВыберите действие: [1] Просмотреть альбом, [2] Создать новый, [0] Назад: ').strip()

                #Просмотр альбома
                if ans == "1":
                    if not service.albums:
                        print("Нет альбомов для просмотра.")
                    else:
                        num = int(input("Введите номер альбома: ")) - 1
                        if 0 <= num < len(service.albums):
                            album = service.albums[num]
                            print(f"\nАльбом: {album.title} ({album.year}) — {album.artist.username}")
                            if album.tracks:
                                print("Треки:")
                                for i, track in enumerate(album.tracks, 1):
                                    print(f"{i}. {track.title} — {track.artist.username}")
                            else:
                                print("В этом альбоме пока нет треков.")

                            action = input("\n[1] Добавить трек, [0] Назад: ").strip()
                            if action == "1":
                                if not service.tracks:
                                    print("Нет треков для добавления.")
                                else:
                                    print("\nДоступные треки:")
                                    for i, t in enumerate(service.tracks, 1):
                                        print(f"{i}. {t}")

                                    tnum = int(input("Выберите трек по номеру: ")) - 1
                                    if 0 <= tnum < len(service.tracks):
                                        track = service.tracks[tnum]

                                        # Проверка на дубликат
                                        if track in album.tracks:
                                            print("Этот трек уже есть в альбоме.")
                                        else:
                                            album.tracks.append(track)
                                            service.albums[num] = album
                                            Terminal.save(filename, type_data, service)  # сохраняем весь сервис
                                            print(f"✅ Трек '{track.title}' добавлен в альбом '{album.title}'")
                                    else:
                                        print("Неверный номер трека.")
                            elif action == "0":
                                pass
                        else:
                            print("Неверный номер альбома.")

                #Создание альбома
                elif ans == "2":
                    title = input("Введите название альбома: ").strip()
                    try:
                        year = int(input("Введите год выпуска: ").strip())
                    except ValueError as v:
                        print(f"Произошла ошибка: {v}\nВ следующий раз введите число")
                        continue

                    #выбор артиста
                    if service.artists:
                        print("\n🎤 Существующие артисты:")
                        for i, artist in enumerate(service.artists, 1):
                            print(f"{i}. {artist.username}")
                        art_choice = input("Выберите артиста по номеру или введите 'новый': ").strip()
                        if art_choice.lower() == "новый":
                            name = input("Имя нового артиста: ")
                            bio = input("Биография: ")
                            artist = Artist(username=name, bio=bio)
                        else:
                            artist = service.artists[int(art_choice) - 1]
                    else:
                        print("Артистов нет — создаём нового 🎤")
                        name = input("Имя артиста: ")
                        bio = input("Биография: ")
                        artist = Artist(username=name, bio=bio)

                    album = Album(tracks=[], title=title, year=year, artist=artist)
                    Terminal.save(filename, type_data, Service(albums=[album], artists=[artist]))
                    print(f"✅ Альбом '{album.title}' добавлен артистом {artist.username}.")

                elif ans == 0:
                    pass

            #Очереди
            elif choice == 7:  
                if service.queues:
                    print("\nОчереди:\n")
                    for i, q in enumerate(service.queues, 1):
                        print(f"{i}. Очередь пользователя {q.user.username} — {len(q.tracks)} трек(ов)")
                else:
                    print("Очередей нет.")

                ans = input('\nВыберите действие: [1] Просмотреть очередь, [2] Создать новую, [0] Назад: ').strip()

                #Просмотр очереди
                if ans == "1":
                    if not service.queues:
                        print("Нет очередей для просмотра.")
                    else:
                        num = int(input("Введите номер очереди: ")) - 1
                        if 0 <= num < len(service.queues):
                            queue = service.queues[num]
                            print(f"\nПользователь: {queue.user.username}")
                            print("Треки в очереди:")
                            if queue.tracks:
                                for i, t in enumerate(queue.tracks, 1):
                                    print(f"{i}. {t.title} — {t.artist.username}")
                            else:
                                print("Очередь пуста.")

                            add_ans = input("\nДобавить трек в очередь? [да/нет]: ").strip().lower()
                            if add_ans == "да":
                                if not service.tracks:
                                    print("Нет треков для добавления.")
                                else:
                                    print("\nДоступные треки:")
                                    for i, t in enumerate(service.tracks, 1):
                                        print(f"{i}. {t.title} — {t.artist.username}")
                                    tnum = int(input("Выберите трек по номеру: ")) - 1
                                    if 0 <= tnum < len(service.tracks):
                                        queue.add_to_queue(service.tracks[tnum])
                                        Terminal.save(filename, type_data, Service(queues=[queue]))
                                        print(f"Трек '{service.tracks[tnum].title}' добавлен в очередь {queue.user.username}.")
                                    else:
                                        print("Неверный выбор трека.")
                        else:
                            print("Неверный номер очереди.")

                #Создание новой очереди
                elif ans == "2":
                    if not service.users:
                        print("Нет пользователей")
                    else:
                        print("\nПользователи:")
                        for i, user in enumerate(service.users, 1):
                            print(f"{i}. {user.username}")
                        u_choice = int(input("Выберите пользователя по номеру: ")) - 1
                        user = service.users[u_choice]

                        tracks = []
                        if service.tracks:
                            add_ans = input("Добавить треки сразу? [да/нет]: ").strip().lower()
                            if add_ans == "да":
                                for i, t in enumerate(service.tracks, 1):
                                    print(f"{i}. {t.title} — {t.artist.username}")
                                nums = input("Введите номера треков через пробел: ").split()
                                for n in nums:
                                    idx = int(n) - 1
                                    if 0 <= idx < len(service.tracks):
                                        tracks.append(service.tracks[idx])

                        queue = Queue(user=user, tracks=tracks)
                        Terminal.save(filename, type_data, Service(queues=[queue], users=[user]))

                        print(f"Очередь для {user.username} успешно создана.")


            #Субтитры
            elif choice == 8:
                if service.lyrics:
                    for i in service.lyrics:
                        print(i)
                else:
                    print("Нет привязанных субтитров")
                ans = input("\nДобавить субтитры к треку? [да/нет]: ")
                if ans.lower() == "да":
                    for i, t in enumerate(service.tracks, 1):
                        print(f"{i}. {t.title}")
                    t_idx = int(input("Выберите трек: ")) - 1
                    track = service.tracks[t_idx]
                    text = input("Введите текст песни: ")
                    lyric = Lyrics(text, track)
                    Terminal.save(filename, type_data, Service(lyrics=[lyric]))
                    print("Субтитры добавлены.")

            #Жанры
            elif choice == 9:
                if service.genres:
                    for i in service.genres:
                        print(i)
                else:
                    print("Нет привязанных жанров")
                ans = input("\nДобавить жанр к треку? [да/нет]: ")
                if ans.lower() == "да":
                    for i, t in enumerate(service.tracks, 1):
                        print(f"{i}. {t.title}")
                    t_idx = int(input("Выберите трек: ")) - 1
                    track = service.tracks[t_idx]
                    gtype = input("Введите жанр: ")
                    genre = Genre(gtype, track)
                    Terminal.save(filename, type_data, Service(genres=[genre]))
                    print("Жанр добавлен.")

            #Тэги
            elif choice == 10:
                if service.tags:
                    for i in service.tags:
                        print(i)
                else:
                    print("Нет привязанных тэгов")
                ans = input("\nДобавить тэг к треку? [да/нет]: ")
                if ans.lower() == "да":
                    for i, t in enumerate(service.tracks, 1):
                        print(f"{i}. {t.title}")
                    t_idx = int(input("Выберите трек: ")) - 1
                    track = service.tracks[t_idx]
                    tag_name = input("Введите тэг: ")
                    tag = Tag(tag_name, track)
                    Terminal.save(filename, type_data, Service(tags=[tag]))
                    print("Тэг добавлен.")


                    

            elif choice == 11:
                filename = input("Введите имя файла: ")
                type_data = filename.split(".")[1]
                try:
                    service = Terminal.load(filename, type_data)
                except Exception as e:
                    filename="music_test.json"
                    type_data="json"
                    print(f"Произошла ошибка: {e}")

            elif choice == 12:
                break

if __name__ == "__main__":              
    Terminal.start_terminal()
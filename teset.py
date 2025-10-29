import random
import string
import json
with open("hospital.json","r",encoding="UTF-8") as f:
    data=json.load(f)

class Generate():
    _lst_polis = ['0125', '3223', '7777']
    _lst_ids = ['M001','T002','T001','X002','K001','S002']

    #создание полиса
    @staticmethod
    def get_polis():
        while True:
            polis = str(random.randint(1000, 9999))
            if polis not in Generate._lst_polis:
                Generate._lst_polis.append(polis)
                return polis
            
    #создание id для врача
    @staticmethod
    def get_code():
        while True:
            code = random.choice(string.ascii_uppercase) + ''.join(random.choices(string.digits, k=4))
            if code not in Generate._lst_ids:
                Generate._lst_ids.append(code)
                return code

#-----------Пациент-----------------
class Patient:
    def __init__(self, polis : str):
        self.polis = polis
    @staticmethod
    def add_patient(name: str, polis: str):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")
            
        if name in data.get("patient_dict", {}):
            print(f"\nПациент '{name}' уже существует")
            return False

        else:
            data["patient_dict"][name] = polis
            print(f"Пациент '{name}' создан! (Полис: {polis})")
            return[polis,name]

    with open("hospital.json","w",encoding="UTF-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def remove_patient(polis1 : str):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")

            # Проверяем наличие блока с пациентами
        if "patient_dict" in data:
            for name, value in list(data["patient_dict"].items()):  # list() чтобы можно было удалять
                if value == polis1:
                    del data["patient_dict"][name]
                    found = True
                    print(f"Пациент с ID {polis1} ({name}) удалён.")
                    break

            with open("hospital.json","w",encoding="UTF-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    def to_dict(self):
        return {
            'ИФО' : self.name,
            'Полис' : self.polis,
        }

    def Work_actions(self,polis):
        while True:
            if input("Показать медицинскую карту (да/нет): ").strip().lower() == 'да':
                print(f"Медицинская карта пациента {polis} :")
                Medical_card.show_medical_card(polis)
                if input('\nНужно ли сделать еще что-то? (да/нет): ').strip().lower() == 'да':
                    continue
                else:
                    break
            else:
                if input("Запись: (да/нет): ").strip().lower() == 'да':
                    Record.work_record(polis = polis)
                    if input('\nНужно ли сделать еще что-то? (да/нет): ').strip().lower() == 'да':
                        continue
                    else:
                        break
                else:
                    if input("Сходить на прием(да/нет): ").strip().lower() == 'да':
                        Reception.start_reception(polis)
                        if input('\nНужно ли сделать еще что-то? (да/нет): ').strip().lower() == 'да':
                            continue
                        else:
                            break
                    else:
                        print("\nВведён неверный запрос! Попробуйте снова.\n")
                        return self.Work_actions(polis)

class Hospital:
    def __init__(self, name : str , addres : str , chief_medical : str , mail : str,doctor_dict: dict, patient_dict: dict):
        self.name = name
        self.addres = addres
        self.chief_medical = chief_medical
        self.mail = mail
        self.doctor = doctor_dict     
        self.patient = patient_dict 
    
    def watch_patient(self):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")

        print("\n=== Список пациентов ===")
        for name, number in data["patient_dict"].items():
            print(f"ФИО: {name} — Номер карты: {number}")

        with open("hospital.json","w",encoding="UTF-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    
    def watch_doctor(self):
        print("\nСписок врачей:")
        for spec in data["doctor_dict"].keys():
            print(f"\nСпециальность : {spec} ")
            for name in data["doctor_dict"].values():
                print(f" - {name} ")
    
    def show_hocpital(self):#выведи инфу про поликлинику
        print(f"\nНазвание: {self.name}\nАдрес: {self.addres}\nГлавный врач: {self.chief_medical}\nПочта: {self.mail}")
        return True

    def Work_patient(self):#Нужно ли вам узнать о врачах
        print("Выберите что хотите сделать: \n")
        while True:
            if input("Хотите узнать информацию о поликлинике?(да/нет) : ").strip().lower() == 'да':
                self.show_hocpital()
                if input('\nНужно ли сделать еще что-то? (да/нет) : ').strip().lower()=='да':
                    continue
                else:
                    break 
            else:
                if input("\nПосмотреть список врачей (да/нет): ").strip().lower() == 'да':
                    self.watch_doctor()
                    if input('\nНужно ли сделать еще что-то? (да/нет) : ').strip().lower()=='да':
                        continue
                    else:
                        break 
                else:
                    if input("\nНе нашли нужного пункта?(да/нет) : ").strip().lower() == 'да':
                        print("\nОтправляйтесь к регистратуре")
                        self.Work_registrashion()
                        break
                    else:
                        if input("\nВыйти?(да/нет): ").strip().lower()=='да':
                            break
                        else:
                            print("\nВведен неверный запрос! Попробуйте снова.\n")
                            return self.Work_patient()  
                        
    def Work_registrashion(self):
        code = input("\nВведи код администратора: ")
        if code=='1111':
            while True:
                if input("\nПросмотр существующих пациентов (да/нет): ").strip().lower() == 'да':
                    self.watch_patient()
                    if input('\nНужно ли сделать еще что-то? (да/нет) : ').strip().lower()=='да':
                        continue
                    else:
                        break
                else:
                    if input("\nДобавить пациента (да/нет): ").strip().lower() == 'да':
                        polis = Generate.get_polis()
                        name = input("Введите ФИО: ").strip()
                        result = Patient.add_patient(name,polis)
                        if result!=False:
                            print("Медицинская карта: ")
                            Medical_card.create_medical_card(result[0],result[1])
                            print(f"Страничка {result[0]} для записей готова")
                            Record.add_record(result[0])
                            if input('\nНужно ли сделать еще что-то? (да/нет) : ').strip().lower()=='да':
                                continue
                            else:
                                break
                        else:
                            if input('\nНужно ли сделать еще что-то? (да/нет) : ').strip().lower()=='да':
                                continue
                            else:
                                break
                    else:
                        if input("\nУдалить пациента(да/нет): ").strip().lower() == 'да':
                            self.watch_patient()
                            polis = input("Введите полис: ").strip()
                            Patient.remove_patient(polis)
                            if input('\nНужно ли сделать еще что-то? (да/нет) : ').strip().lower()=='да':
                                continue
                            else:
                                break 
                        else:
                            if input("\nДобавить врача (да/нет): ").strip().lower()=='да':
                                self.watch_doctor()
                                name_dc = input("Введите ИФО: ").strip()
                                spec_ds = input("Введите специальность: ").strip()
                                Specialization_and_oficce.add_spec_and_oficce(spec_ds)
                                ids = Generate.get_code()
                                obj = Doctor.add_doctor(spec_ds,name_dc,ids)
                                Free_days.create_free_days(obj)
                                if input('\nНужно ли сделать еще что-то? (да/нет) : ').strip().lower()=='да':
                                    continue
                                else:
                                    break 
                            else:
                                if input("\nИменить график работы врачей?(да/нет): ").strip().lower()=='да':
                                    ...
                                    if input('\nНужно ли сделать еще что-то? (да/нет) : ').strip().lower()=='да':
                                        continue
                                    else:
                                        break 
                                else:
                                    if input("Выйти?(да/нет): ").strip().lower()=='да':
                                        break
                                    else:
                                        print("\nВведен неверный запрос! Попробуйте снова.\n")
                                        return self.Work_patient()
        else:
            if input("\nВведен неверный код!Попробовать заново(да/нет): ").strip().lower()=='да':
                self.Work_registrashion()
            else:
                print('\nОшибка входа')
                return

    def choose_patient(self):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")

        print("===Список пациентов===")
        for name, number in data["patient_dict"].items():
            print(f"ФИО: {name} - ID: {number}")

        object = input("\nВведите ID пациента: ")
        for name, number in data["patient_dict"].items():
            if number == object:
                print(f"\nВы выбрали пациента: {name} (ID: {number})")
                result = number
                return result #наш пациент 

        if input("\nПациент не найден. Повторить попытку снова?(да/нет): ").strip().lower()=='да':
            return self.choose_patient()    
        else:
            print("\nДо встречи :))))")
            return 

#--------------Диагноз----------
class Diagnosis:
    try:
        with open("hospital.json","r",encoding="UTF-8") as f:
            data=json.load(f)
    except FileNotFoundError:
        print("\nФайл не найден!")
    
    def write_diagnos(polis:str):
        name = input("Название диагноза: ")
        data = input("Введите дату (01/02/2006)")
        comment = input("Введите комментарии по лечению : ")
        data["medical_cards"][polis]["Диагнозы"][name] = [data,comment]
        with open("hospital.json","w",encoding="UTF-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

#--------------Медицинская карта----------
class Medical_card:
    @staticmethod
    def create_medical_card(polis: str, name: str):
        try:
            with open("hospital.json", "r", encoding="UTF-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")
            return

        # Получаем данные от пользователя
        gender = input("Введите пол (женский/мужской): ")
        birthday = input("Введите дату рождения (02.04.2000): ")
        phone = input("Введите номер телефона (+7-777-777-70-70): ")

        # Создаем структуру медицинской карты
        data["medical_cards"][polis] = {
            "ФИО": name,
            "Пол": gender,
            "Дата рождения": birthday,
            "Номер телефона": phone,
            "Диагнозы": {}
        }

        with open("hospital.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Медицинская карта для {name} (полис {polis}) успешно создана!")

    def add_diagnosis(self,diagnos : Diagnosis, patient : Patient ,medical_cards : dict):
        self.all_keys = []
        self.polis = patient.polis
        self.name = diagnos.name
        self.data = diagnos.data
        self.comment = diagnos.comment
        for k in medical_cards.keys():
            self.all_keys.append(k)
        if self.name in self.all_keys:
            print("Поименяйте название диагноза! ")
        else:
            medical_cards[self.polis][self.name] = [self.data,self.comment]
            print("Диагноз записан в медкижку ")
        return


    @staticmethod
    def show_medical_card(polis: str):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")

        if polis not in data["medical_cards"]:
            print(f"Карта с полисом {polis} не найдена.")
            return

        card = data["medical_cards"][polis]
        print(f"\n====Медицинская карта пациента (полис {polis})====:")
        for key, value in card.items():
            # если это раздел "Диагнозы" — обрабатываем отдельно
            if key == "Диагнозы":
                print(f"  {key}:")
                for diagnosis, info in value.items():
                    print(f"  - {diagnosis}")
                    print(f"   Дата постановки: {info[0]}")
                    print(f"   Показания: {info[1]}")
            else:
                print(f"  {key}: {value}")

#--------------Направление-------
class Direction:
    def show_medical_card(polis: str):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")

    def provide_a_referral(polis : str):
        all_cpec = ["терапевт","стоматолог","хирург"]
        spec = input("Введите Специальность(терапевт,стоматолог,хирург): ").strip().lower()
        term = input("Введите срок").strip().lower()
        if spec in all_cpec:
            data["record_dict"][polis]['направления']=[spec,term]
            print("Направление записано в очерь записей")
            with open("hospital.json","w",encoding="UTF-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

#--------Специализация и кабинет---------
class Specialization_and_oficce:
    def __init__(self,spec,office,spetcial: dict):
        self.spec = spec
        self.office = office
        self.spetcial = spetcial

    def add_spec_and_oficce(spec :str):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")
        all_spec = []
        all_cabin = []
        for k,n in data["spetcial_and_office"].items():
            all_spec.append(k)
            all_cabin.append(n)
        if spec in all_spec:
            print("Врач с такой спечальность сущетсвует ")
            return True
        else:
            print(f"Занятые кабинеты : {all_cabin}")
            cabin = input("Введите кабинет(015): ")
            data["spetcial_and_office"][spec] = cabin
            print("Специальность добавлена")
            with open("hospital.json","w",encoding="UTF-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def choose_spetcial():
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")
        print('Доступные специальности:')
        all_spec = []
        for k in data["spetcial_and_office"].keys():
            all_spec.append(k)
            print(f" - {k}")

        spec = input('Введите выбранную специальность: ').strip().lower()

        if spec in all_spec:
            office = data["spetcial_and_office"][spec]
            print(f"Вы выбрали: {spec} (кабинет{office})")
            with open("hospital.json","w",encoding="UTF-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return [spec, office]
        else:
            print("Такой специальности нет, попробуйте снова.")
            return Specialization_and_oficce.choose_spetcial()
        
#--------Doctor------------
class Doctor:
    def __init__(self,doctor_dict: dict,specialization: Specialization_and_oficce,name,doctor_id):
        self.doctor_dict = doctor_dict
        self.spec = specialization.spec
        self.name = name 
        self.doctor_id = doctor_id
        
    @staticmethod
    def add_doctor(spec: str,name: str , ids : str):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")
            
        if name in data.get("doctor_dict", {}):
            print(f"\nВрач '{name}' уже существует")
            return
        else:
            if spec not in data.get("doctor_dict", {}):
                data["doctor_dict"][spec]={}
            
            data["doctor_dict"][spec][name] = ids
            with open("hospital.json","w",encoding="UTF-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Врач '{name}' создан! (Внутренний номер: {ids})")
            return ids
        
        #создание графика работы

    @staticmethod
    def choose_doctor(spec:str):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")

        print(f"\nСписок врачей по специальности '{spec}':")
        for name, doc_id in data["doctor_dict"][spec].items():
            print(f"ID: {doc_id} — {name}")

        doctor_id = input("\nВведите ID врача: ").strip().upper()
        all_ID = []
        # Поиск врача по ID
        for doc_id in data["doctor_dict"][spec].values():
            all_ID.append(doc_id)

        if doctor_id in all_ID:
            print(f"Вы выбрали врача: {name} ")
            with open("hospital.json","w",encoding="UTF-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return [name, doctor_id]
        else:
            print("Врач с таким ID не найден. Попробуйте снова.")
            return Doctor.choose_doctor()
    
        
#--------------Расписание--------
class Free_days:
    def __init__(self, data, time, doctor, free_days: dict):
        self.data = data
        self.time = time
        self.doctor = doctor
        self.free_days = free_days
    
    def create_free_days(ids):
        try:
            with open("hospital.json", "r", encoding="UTF-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")
            return
        
        data["free_days"][ids] = {}
        print("Врач внесен в график)")
        with open("hospital.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def choose_a_day(ids : str):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")

        for datas,time in data["free_days"][ids].items():
            print(f"Дата:{datas} - Время:{time}")

        Data = input("Введите дату : ")
        Time = input("Введите время: ")

        # Проверка, что день и время существуют
        if Data in data["free_days"][ids].keys() and Time in data["free_days"][ids].values():
            result = [Data, Time]
            data["free_days"][ids][Data].remove(Time)
            print(f"Запись на {Data} в {Time} создана")
            return result
        else:
            print("Такого времени нет.")

        for k in list(data["free_days"][ids].keys()):
            for day, times in data["free_days"][k].items():
                if times == []:  
                    del data["free_days"][ids][day]
                    print(f"Удалён пустой день {day} для врача {ids}")

        with open("hospital.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


    def add_time(self, ids: str, free_days: dict):
        self.free_days = free_days
        self.ids = ids
        print("\nВыберите день: ")
        all_days = list(self.free_days[self.ids].keys())
        for k in all_days:
            print(f"День : {k}")
        request1 = input("\nВыбранный день ('29.06.2025'): ").strip()
        if request1 not in all_days:
            print("\nВведите заново: ")
            self.add_time(self.ids, self.free_days)
        else:
            request2 = input("\nВведите время ('12:00'): ").strip()
            self.free_days[self.ids][request1].append(request2)
            print(f"Добавлено время {request2} для дня {request1}")

    def add_day(self, ids: str, free_days: dict):
        self.free_days = free_days
        self.ids = ids
        all_days = list(self.free_days[self.ids].keys())
        all_time = sum(self.free_days[self.ids].values(), [])

        print("\nТекущее расписание:")
        for k, n in self.free_days[self.ids].items():
            print(f"День : {k} - {n}")

        request1 = input("\nВведите число ('29.01.2025'): ").strip()
        if request1 not in all_days:
            request2 = input("Введите время ('12:00'): ").strip()
            if request2 not in all_time:
                self.free_days[self.ids][request1] = [request2]
                print(f"Добавлен день {request1} с временем {request2}")
            else:
                print("Такое время уже занято, попробуйте снова.")
                self.add_day(self.ids, self.free_days)
        else:
            print("Такой день уже есть, попробуйте снова.")
            self.add_day(self.ids, self.free_days)

    def remove_time(self, ids: str, free_days: dict):
        self.free_days = free_days
        self.ids = ids
        print("\nВыберите день: ")
        all_days = list(self.free_days[self.ids].keys())
        for k in all_days:
            print(f"День : {k}")
        request1 = input("\nВыбранный день ('29.06.2025'): ").strip()

        if request1 not in all_days:
            print("\nВведите заново: ")
            self.remove_time(self.ids, self.free_days)
        else:
            print(f"Доступное время для {request1}: {self.free_days[self.ids][request1]}")
            request2 = input("\nВведите время ('12:00'): ").strip()

            if request2 in self.free_days[self.ids][request1]:
                self.free_days[self.ids][request1].remove(request2)
                print(f"Удалено время {request2} для дня {request1}")
                if not self.free_days[self.ids][request1]:
                    del self.free_days[self.ids][request1]
                    print(f"День {request1} удалён, так как в нём не осталось времени.")
            else:
                print("Такого времени нет, попробуйте снова.")
                self.remove_time(self.ids, self.free_days)

    def remove_day(self, ids: str, free_days: dict):
        self.free_days = free_days
        self.ids = ids
        all_days = list(self.free_days[self.ids].keys())

        for k, n in self.free_days[self.ids].items():
            print(f"День : {k} - {n}")

        request1 = input("\nВведите день для удаления ('29.01.2025'): ").strip()
        if request1 in all_days:
            confirm = input(f"Удалить день {request1}? (y/n): ").strip().lower()
            if confirm == 'y':
                del self.free_days[self.ids][request1]
                print(f"День {request1} успешно удалён.")
            else:
                print("Удаление отменено.")
        else:
            print("Такого дня нет, попробуйте снова.")
            self.remove_day(self.ids, self.free_days)

    def add_report(self, ids: str, free_days: dict):
        self.ids = ids
        self.free_days = free_days
        for k, n in self.free_days[self.ids].items():
            print(f"День : {k} - Время: {n}")
        request = input("\nХотите добавить дату или время (дата/время): ").strip().lower()
        if request == 'время':
            self.add_time(self.ids, self.free_days)
        elif request == 'дата':
            self.add_day(self.ids, self.free_days)
        else:
            print("Неверный запрос. Введите заново: ")
            self.add_report(self.ids, self.free_days)

    def remove_record(self, ids: str, free_days: dict):
        self.ids = ids
        self.free_days = free_days
        for k, n in self.free_days[self.ids].items():
            print(f"День : {k} - Время: {n}")
        request = input("\nХотите удалить дату или время (дата/время): ").strip().lower()
        if request == 'время':
            self.remove_time(self.ids, self.free_days)
        elif request == 'дата':
            self.remove_day(self.ids, self.free_days)
        else:
            print("Неверный запрос. Введите заново: ")
            self.remove_record(self.ids, self.free_days)

    def work_free_days(self):
        while True:
            action = input("Добавить или удалить день/время? (добавить/удалить/выход): ").strip().lower()
            if action == 'добавить':
                ids = input("Введите ID врача: ")
                self.add_report(ids, self.free_days)
            elif action == 'удалить':
                ids = input("Введите ID врача: ")
                self.remove_record(ids, self.free_days)
            elif action == 'выход':
                print("Выход из режима администратора.")
                break
            else:
                print("Неверный запрос. Попробуйте снова.")
#------------Запись------------
class Record:
    @staticmethod
    def add_record(polic:str):
        try:
            with open("hospital.json", "r", encoding="UTF-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")

        data["record_dict"][polic] = {
                    'терапевт': [],
                    'хирург' : [],
                    'стоматолог':[],
                }
        with open("hospital.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    #создание записи
    @staticmethod
    def create_record(polis : str):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")

        all_docotor = []
        for k in data["record_dict"][polis].keys():
            all_docotor.append(k)

        spec_office = Specialization_and_oficce.choose_spetcial()#[spec, office]
        doctor = Doctor.choose_doctor(spec_office[0])#[name, doctor_id]
        free_time = Free_days.choose_a_day(doctor[1])#[Data, Time]

        if spec_office[0] in all_docotor:
            print("Запись к этому врачу уже существует! Сначала удалите старую.")
            return
        else:
            data["record_dict"][polis][spec_office[0]] = [
                doctor[0],
                free_time[0],
                free_time[1],
                spec_office[1]
            ]
            print(f"Запись к {spec_office[0]} ({doctor[0]}) успешно создана!")

        with open("hospital.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    #удалить запись
    def remove_record(polis : str):
        try:
            with open("hospital.json","r",encoding="UTF-8") as f:
                data=json.load(f)
        except FileNotFoundError:
            print("\nФайл не найден!")

        all_record_polic = []
        for k in data["record_dict"][polis].keys():
            all_record_polic.append(k)

        print('Выбери специальность: ')
        print(all_record_polic)
        spec = input("Выбаннаая специальность: ").strip().lower()
        if spec in all_record_polic:
            print("Запись пациента удалена")
            del data["record_dict"][polis][spec]
        else:
            print("Такой записи нет ")

        with open("hospital.json", "w", encoding="UTF-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


    def work_record(polis : str):
        print("\nВыберите что хотите сделать : ")
        while True:
            if input("\nХотите добавить запись : (да/нет): ").strip().lower()=='да':
               Record.create_record(polis)
               if input('\nНужно ли сделать еще что-то? (да/нет) : ').strip().lower()=='да':
                    continue
               else:
                    break 
            else:
                if input("Хотите удалить запись (да/нет) : ").strip().lower()=='да':
                    Record.remove_record(polis)
                    if input('\nНужно ли сделать еще что-то? (да/нет) : ').strip().lower()=='да':
                        continue
                    else:
                        break 
                else:
                    if input("\nВведен неверный запрос! Попробуете снова?\n").strip()=='да':
                        print("\nВведен неверный запрос! Попробуйте снова.\n")
                        Record.work_record(polis)  
                    else:
                        break

#--------------Прием----------
class Reception:
    def __init__(self,date, time, doctor,  patient : Patient,record_dict : dict):
        self.date = date
        self.time = time 
        self.doctor = doctor
        self.polis = patient.polis
        self.record_dict = record_dict

    @staticmethod
    def start_reception(polis):
        all_doctor = ['терапевт','стоматолог','хирург']
        number = input("Введите полис: ").strip().lower()
        if number==polis:
            for k,n in data["record_dict"]["polis"].items():
                print(f"Врач: {k} - запись : {n}")
            choose2 = input("Выбрать врача: (терапевт/стоматолог/хирург): ")
            if choose2 in all_doctor:
                print("Удаление записи: ")
                Record.remove_record(polis)
                print("Постановка диагноза: ")
                Diagnosis.write_diagnos()
                if input("Нужно ли направление (да/нет)?").strip().lower()=='да':
                    Direction.provide_a_referral(polis)

if __name__ == "__main__":
    pass
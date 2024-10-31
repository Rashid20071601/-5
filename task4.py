import hashlib  # Библиотека для хеширования данных (используется для защиты паролей)
import time     # Библиотека для работы со временем (позволяет делать паузы)

# Класс пользователя на платформе
class User:
    def __init__(self, nickname, password, age):
        # Уникальные данные пользователя: никнейм и возраст
        self.nickname = nickname
        # Сохраняем хэшированный пароль для безопасности
        self.password = int(hashlib.sha256(password.encode()).hexdigest(), 16)
        self.age = age

    # Метод для представления пользователя в строковом виде
    def __str__(self):
        return f"{self.nickname}, {self.age} лет."

    # Проверка правильности введенного пароля
    def check_password(self, password):
        return self.password == int(hashlib.sha256(password.encode()).hexdigest(), 16)


# Класс для видео на платформе
class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title               # Название видео
        self.duration = duration         # Продолжительность видео в секундах
        self.time_now = 0                # Текущая секунда воспроизведения (изначально 0)
        self.adult_mode = adult_mode     # Ограничение по возрасту (если True — только 18+)

    # Метод для строкового представления видео
    def __str__(self):
        return self.title


# Класс платформы UrTube
class UrTube:
    def __init__(self):
        self.users = []            # Список зарегистрированных пользователей
        self.videos = []           # Список добавленных видео
        self.current_user = None   # Текущий вошедший пользователь (изначально отсутствует)

    # Регистрация нового пользователя
    def register(self, nickname, password, age):
        # Проверяем, существует ли пользователь с таким никнеймом
        if nickname in (user.nickname for user in self.users):
            print(f"Пользователь {nickname} уже существует!")
            return
        # Создаем нового пользователя и добавляем его в список
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user   # Выполняем вход автоматически

    # Вход в учетную запись пользователя
    def log_in(self, nickname, password):
        for user in self.users:
            # Ищем пользователя по имени и паролю
            if user.nickname == nickname and user.check_password(password):
                self.current_user = user
                return
        print("Неверное имя пользователя или пароль")  # Сообщение при ошибке

    # Выход из учетной записи пользователя
    def log_out(self):
        self.current_user = None  # Сбрасываем текущего пользователя

    # Добавление одного или нескольких видео на платформу
    def add(self, *videos):
        for video in videos:
            # Проверка на уникальность названия видео
            if video.title not in (v.title for v in self.videos):
                self.videos.append(video)

    # Поиск видео по ключевому слову (регистр не учитывается)
    def get_videos(self, search_word):
        search_word = search_word.lower()  # Приводим поисковое слово к нижнему регистру
        # Возвращаем список всех названий видео, содержащих поисковое слово
        return [video.title for video in self.videos if search_word in video.title.lower()]

    # Просмотр видео по названию
    def watch_video(self, title):
        # Проверка на вход в учетную запись
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        for video in self.videos:
            # Проверка точного совпадения названия видео
            if video.title == title:
                # Проверка возраста пользователя для контента 18+
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    return
                # Воспроизведение видео (по 1 секунде с паузой)
                for sec in range(1, video.duration + 1):
                    print(sec, end=" ")
                    time.sleep(1)  # Пауза на 1 секунду
                print("Конец видео")
                video.time_now = 0  # Сброс времени просмотра
                return
        print("Видео не найдено")  # Сообщение, если видео не найдено


# Примеры работы программы

# Создаем платформу UrTube и видео
ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео на платформу
ur.add(v1, v2)

# Поиск видео по ключевым словам
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастные ограничения
ur.watch_video('Для чего девушкам парень программист?')  # Без входа
ur.register('vasya_pupkin', 'lolkekcheburek', 13)         # Регистрация пользователя
ur.watch_video('Для чего девушкам парень программист?')    # Возрастное ограничение
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25) # Вход взрослого пользователя
ur.watch_video('Для чего девушкам парень программист?')    # Воспроизведение

# Повторная регистрация пользователя
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизвести несуществующее видео
ur.watch_video('Лучший язык программирования 2024 года!')







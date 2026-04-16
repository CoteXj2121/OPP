from __future__ import annotations

import time
from abc import ABC, abstractmethod


# Task 1
class FileService(ABC):
    @abstractmethod
    def read(self, filename: str) -> str:
        pass

    @abstractmethod
    def write(self, filename: str, content: str) -> str:
        pass


class RealFileService(FileService):
    def read(self, filename: str) -> str:
        return f"Reading {filename}"

    def write(self, filename: str, content: str) -> str:
        return f"Writing {filename}: {content}"


class SecureFileProxy(FileService):
    def __init__(self, service: FileService, role: str):
        self.service = service
        self.role = role

    def read(self, filename: str) -> str:
        if self.role not in {"reader", "admin"}:
            raise PermissionError("Нет прав на чтение")
        return self.service.read(filename)

    def write(self, filename: str, content: str) -> str:
        if self.role != "admin":
            raise PermissionError("Нет прав на запись")
        return self.service.write(filename, content)


# Task 2
class Image(ABC):
    @abstractmethod
    def display(self) -> str:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass


class HighResImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        print(f"Загрузка изображения {filename}")

    def display(self) -> str:
        return f"Display {self.filename}"

    def get_info(self) -> str:
        return f"Info {self.filename}"


class LazyImageProxy(Image):
    def __init__(self, filename: str):
        self.filename = filename
        self._image: HighResImage | None = None

    def _ensure_loaded(self) -> HighResImage:
        if self._image is None:
            self._image = HighResImage(self.filename)
        return self._image

    def display(self) -> str:
        return self._ensure_loaded().display()

    def get_info(self) -> str:
        return self._ensure_loaded().get_info()


# Task 3
class UserService(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> dict:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> str:
        pass


class RealUserService(UserService):
    def get_user(self, user_id: int) -> dict:
        return {"id": user_id, "name": "Анна"}

    def delete_user(self, user_id: int) -> str:
        return f"User {user_id} deleted"


class LoggingUserServiceProxy(UserService):
    def __init__(self, service: UserService):
        self.service = service

    def _log(self, label: str, action):
        start = time.perf_counter()
        try:
            result = action()
            print(f"{label} -> {result} ({time.perf_counter() - start:.6f}s)")
            return result
        except Exception as error:
            print(f"{label} -> {error} ({time.perf_counter() - start:.6f}s)")
            raise

    def get_user(self, user_id: int) -> dict:
        return self._log(f"get_user({user_id})", lambda: self.service.get_user(user_id))

    def delete_user(self, user_id: int) -> str:
        return self._log(f"delete_user({user_id})", lambda: self.service.delete_user(user_id))


# Task 4
class WeatherService(ABC):
    @abstractmethod
    def get_weather(self, city: str) -> str:
        pass


class RealWeatherService(WeatherService):
    def get_weather(self, city: str) -> str:
        return f"Weather in {city}: +20"


class CachedWeatherProxy(WeatherService):
    def __init__(self, service: WeatherService, ttl: float):
        self.service = service
        self.ttl = ttl
        self.cache: dict[str, tuple[str, float]] = {}
        self.hits = 0
        self.misses = 0

    def get_weather(self, city: str) -> str:
        item = self.cache.get(city)
        now = time.time()
        if item is not None:
            value, expires_at = item
            if now < expires_at:
                self.hits += 1
                return value
        self.misses += 1
        value = self.service.get_weather(city)
        self.cache[city] = (value, now + self.ttl)
        return value

    def get_cache_stats(self) -> dict[str, int]:
        return {"hits": self.hits, "misses": self.misses}


# Task 5
class Database(ABC):
    @abstractmethod
    def connect(self) -> str:
        pass

    @abstractmethod
    def query(self, sql: str) -> str:
        pass

    @abstractmethod
    def disconnect(self) -> str:
        pass


class RealDatabase(Database):
    def __init__(self):
        self.connected = False

    def connect(self) -> str:
        self.connected = True
        return "DB connected"

    def query(self, sql: str) -> str:
        return f"Query: {sql}"

    def disconnect(self) -> str:
        self.connected = False
        return "DB disconnected"


class SmartDatabaseProxy(Database):
    def __init__(self, database: RealDatabase, max_connections: int):
        self.database = database
        self.max_connections = max_connections
        self.active_connections = 0

    def _measure(self, label: str, action):
        start = time.perf_counter()
        result = action()
        print(f"{label}: {time.perf_counter() - start:.6f}s")
        return result

    def connect(self) -> str:
        if self.active_connections >= self.max_connections:
            raise RuntimeError("Превышен лимит подключений")

        def action():
            self.active_connections += 1
            if self.active_connections == 1:
                return self.database.connect()
            return f"Connection reused ({self.active_connections})"

        return self._measure("connect", action)

    def query(self, sql: str) -> str:
        return self._measure("query", lambda: self.database.query(sql))

    def disconnect(self) -> str:
        def action():
            if self.active_connections == 0:
                return "Нет активных подключений"
            self.active_connections -= 1
            if self.active_connections == 0:
                return self.database.disconnect()
            return f"Connections left: {self.active_connections}"

        return self._measure("disconnect", action)


if __name__ == "__main__":
    print("Task 1")
    admin = SecureFileProxy(RealFileService(), "admin")
    print(admin.read("report.txt"))
    print(admin.write("report.txt", "hello"))
    print("-" * 40)

    print("Task 2")
    images = [LazyImageProxy(f"img_{index}.png") for index in range(3)]
    print(images[0].display())
    print(images[1].get_info())
    print("-" * 40)

    print("Task 3")
    user_service = LoggingUserServiceProxy(RealUserService())
    print(user_service.get_user(1))
    print(user_service.delete_user(1))
    print("-" * 40)

    print("Task 4")
    weather = CachedWeatherProxy(RealWeatherService(), ttl=5)
    print(weather.get_weather("Moscow"))
    print(weather.get_weather("Moscow"))
    print(weather.get_cache_stats())
    print("-" * 40)

    print("Task 5")
    database = SmartDatabaseProxy(RealDatabase(), max_connections=2)
    print(database.connect())
    print(database.connect())
    print(database.query("SELECT * FROM users"))
    print(database.disconnect())
    print(database.disconnect())

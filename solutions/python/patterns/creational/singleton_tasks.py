from __future__ import annotations

import time


class SingletonMeta(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# Task 1
class AppConfig(metaclass=SingletonMeta):
    def __init__(self, settings: dict[str, str] | None = None):
        if not hasattr(self, "_settings"):
            self._settings = dict(settings or {})

    def get(self, key: str):
        return self._settings.get(key)

    def set(self, key: str, value):
        self._settings[key] = value


# Task 2
class ConnectionPool(metaclass=SingletonMeta):
    def __init__(self, max_connections: int = 2):
        if hasattr(self, "_initialized"):
            return
        self.max_connections = max_connections
        self._available: list[str] = []
        self._in_use: set[str] = set()
        self._created = 0
        self._initialized = True

    def acquire(self) -> str:
        if self._available:
            connection = self._available.pop()
            self._in_use.add(connection)
            return connection
        if self._created >= self.max_connections:
            raise RuntimeError("Нет свободных соединений")
        self._created += 1
        connection = f"connection-{self._created}"
        self._in_use.add(connection)
        return connection

    def release(self, connection: str) -> None:
        if connection in self._in_use:
            self._in_use.remove(connection)
            self._available.append(connection)


# Task 3
class EventCounter(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, "_events"):
            self._events: dict[str, int] = {}

    def increment(self, event: str) -> None:
        self._events[event] = self._events.get(event, 0) + 1

    def decrement(self, event: str) -> None:
        if event in self._events and self._events[event] > 0:
            self._events[event] -= 1

    def get(self, event: str) -> int:
        return self._events.get(event, 0)

    def reset(self, event: str) -> None:
        self._events[event] = 0


# Task 4
class MemoryCache(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, "_store"):
            self._store: dict[str, tuple[object, float]] = {}

    def set(self, key: str, value, ttl: float) -> None:
        self._store[key] = (value, time.time() + ttl)

    def get(self, key: str):
        item = self._store.get(key)
        if item is None:
            return None
        value, expires_at = item
        if time.time() > expires_at:
            del self._store[key]
            return None
        return value

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def flush(self) -> None:
        self._store.clear()


# Task 5
class FeatureFlagManager(metaclass=SingletonMeta):
    def __init__(self, flags: dict[str, bool] | None = None):
        if not hasattr(self, "_flags"):
            self._flags = dict(flags or {})

    def _ensure_exists(self, flag: str) -> None:
        if flag not in self._flags:
            raise KeyError(f"Флаг {flag} не существует")

    def is_enabled(self, flag: str) -> bool:
        self._ensure_exists(flag)
        return self._flags[flag]

    def enable(self, flag: str) -> None:
        self._ensure_exists(flag)
        self._flags[flag] = True

    def disable(self, flag: str) -> None:
        self._ensure_exists(flag)
        self._flags[flag] = False

    def get_all(self) -> dict[str, bool]:
        return dict(self._flags)


if __name__ == "__main__":
    print("Task 1")
    config1 = AppConfig({"env": "dev"})
    config2 = AppConfig()
    config2.set("debug", "true")
    print(config1 is config2, config1.get("env"), config2.get("debug"))
    print("-" * 40)

    print("Task 2")
    pool = ConnectionPool(max_connections=2)
    c1 = pool.acquire()
    c2 = pool.acquire()
    print(c1, c2)
    pool.release(c1)
    print(pool.acquire())
    print("-" * 40)

    print("Task 3")
    counter1 = EventCounter()
    counter2 = EventCounter()
    counter1.increment("login")
    counter2.increment("login")
    print(counter1.get("login"))
    print("-" * 40)

    print("Task 4")
    cache = MemoryCache()
    cache.set("article:1", {"title": "Новость"}, ttl=1)
    print(cache.get("article:1"))
    time.sleep(1.1)
    print(cache.get("article:1"))
    print("-" * 40)

    print("Task 5")
    flags1 = FeatureFlagManager({"beta_ui": False, "new_search": True})
    flags2 = FeatureFlagManager()
    flags2.enable("beta_ui")
    print(flags1 is flags2, flags1.get_all())

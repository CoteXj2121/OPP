from abc import ABC, abstractmethod


class ReadableStorage(ABC):
    @abstractmethod
    def read(self, key: str) -> str:
        pass


class WritableStorage(ReadableStorage):
    @abstractmethod
    def write(self, key: str, value: str) -> None:
        pass


class InMemoryStorage(WritableStorage):
    def __init__(self):
        self._data: dict[str, str] = {}

    def read(self, key: str) -> str:
        return self._data.get(key, "")

    def write(self, key: str, value: str) -> None:
        self._data[key] = value
        print(f"Запись: {key} = {value}")


class ReadOnlyStorage(ReadableStorage):
    def __init__(self, data: dict[str, str]):
        self._data = data

    def read(self, key: str) -> str:
        return self._data.get(key, "")


def save_data(storage: WritableStorage, key: str, value: str) -> None:
    storage.write(key, value)
    print(storage.read(key))


if __name__ == "__main__":
    writable = InMemoryStorage()
    save_data(writable, "user", "Алексей")

    readonly = ReadOnlyStorage({"user": "Анна"})
    print(readonly.read("user"))

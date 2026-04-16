from abc import ABC, abstractmethod


class Reader(ABC):
    @abstractmethod
    def read(self, path: str) -> str:
        pass


class FileReader(Reader):
    def read(self, path: str) -> str:
        return f"Содержимое файла: {path}"


class NetworkFileReader(Reader):
    def __init__(self, available: bool):
        self.available = available

    def read(self, path: str) -> str:
        if not self.available:
            return f"Сеть недоступна для файла {path}"
        return f"Содержимое по сети: {path}"


def process(reader: Reader, path: str) -> None:
    content = reader.read(path)
    print(content.upper())


if __name__ == "__main__":
    process(FileReader(), "local.txt")
    process(NetworkFileReader(available=True), "remote.txt")
    process(NetworkFileReader(available=False), "remote.txt")

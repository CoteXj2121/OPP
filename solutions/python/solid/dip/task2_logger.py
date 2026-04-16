from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


class FileLogger(Logger):
    def log(self, message: str) -> None:
        print(f"[FILE] {message}")


class ConsoleLogger(Logger):
    def log(self, message: str) -> None:
        print(f"[CONSOLE] {message}")


class UserService:
    def __init__(self, logger: Logger):
        self.logger = logger

    def register(self, username: str) -> None:
        print(f"Пользователь {username} зарегистрирован")
        self.logger.log(f"Регистрация: {username}")

    def delete(self, username: str) -> None:
        print(f"Пользователь {username} удален")
        self.logger.log(f"Удаление: {username}")


if __name__ == "__main__":
    file_service = UserService(FileLogger())
    console_service = UserService(ConsoleLogger())

    file_service.register("Алексей")
    console_service.delete("Алексей")

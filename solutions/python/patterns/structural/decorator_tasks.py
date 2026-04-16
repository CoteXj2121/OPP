from __future__ import annotations

import base64
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable


# Task 1
class TextMessage(ABC):
    @abstractmethod
    def get_content(self) -> str:
        pass


class PlainTextMessage(TextMessage):
    def __init__(self, content: str):
        self.content = content

    def get_content(self) -> str:
        return self.content


class TextDecorator(TextMessage):
    def __init__(self, wrapped: TextMessage):
        self.wrapped = wrapped


class UpperCaseDecorator(TextDecorator):
    def get_content(self) -> str:
        return self.wrapped.get_content().upper()


class TrimDecorator(TextDecorator):
    def get_content(self) -> str:
        return self.wrapped.get_content().strip()


class CensorDecorator(TextDecorator):
    def __init__(self, wrapped: TextMessage, banned_words: list[str]):
        super().__init__(wrapped)
        self.banned_words = banned_words

    def get_content(self) -> str:
        text = self.wrapped.get_content()
        for word in self.banned_words:
            text = text.replace(word, "***")
        return text


class LengthLimitDecorator(TextDecorator):
    def __init__(self, wrapped: TextMessage, limit: int):
        super().__init__(wrapped)
        self.limit = limit

    def get_content(self) -> str:
        return self.wrapped.get_content()[: self.limit]


# Task 2
@dataclass
class Request:
    method: str
    url: str
    headers: dict[str, str] = field(default_factory=dict)
    body: str | None = None


@dataclass
class Response:
    status_code: int
    body: str


class HttpClient(ABC):
    @abstractmethod
    def send(self, request: Request) -> Response:
        pass


class SimpleHttpClient(HttpClient):
    def __init__(self):
        self._attempts: dict[str, int] = {}

    def send(self, request: Request) -> Response:
        self._attempts[request.url] = self._attempts.get(request.url, 0) + 1
        if "retry" in request.url and self._attempts[request.url] == 1:
            return Response(500, "temporary error")
        return Response(200, f"{request.method} {request.url}")


class HttpClientDecorator(HttpClient):
    def __init__(self, wrapped: HttpClient):
        self.wrapped = wrapped


class AuthDecorator(HttpClientDecorator):
    def __init__(self, wrapped: HttpClient, token: str):
        super().__init__(wrapped)
        self.token = token

    def send(self, request: Request) -> Response:
        request.headers["Authorization"] = f"Bearer {self.token}"
        return self.wrapped.send(request)


class LoggingDecorator(HttpClientDecorator):
    def send(self, request: Request) -> Response:
        print(f"Request: {request.method} {request.url}")
        response = self.wrapped.send(request)
        print(f"Response: {response.status_code}")
        return response


class RetryDecorator(HttpClientDecorator):
    def __init__(self, wrapped: HttpClient, retries: int):
        super().__init__(wrapped)
        self.retries = retries

    def send(self, request: Request) -> Response:
        last_response = Response(500, "no response")
        for _ in range(self.retries + 1):
            last_response = self.wrapped.send(request)
            if last_response.status_code < 500:
                return last_response
        return last_response


class CachingDecorator(HttpClientDecorator):
    def __init__(self, wrapped: HttpClient):
        super().__init__(wrapped)
        self.cache: dict[str, Response] = {}

    def send(self, request: Request) -> Response:
        if request.method == "GET" and request.url in self.cache:
            return self.cache[request.url]
        response = self.wrapped.send(request)
        if request.method == "GET" and response.status_code == 200:
            self.cache[request.url] = response
        return response


# Task 3
class DataStream(ABC):
    @abstractmethod
    def write(self, data: str) -> None:
        pass

    @abstractmethod
    def read(self) -> str:
        pass


class MemoryStream(DataStream):
    def __init__(self):
        self.data = ""

    def write(self, data: str) -> None:
        self.data = data

    def read(self) -> str:
        return self.data


class StreamDecorator(DataStream):
    def __init__(self, wrapped: DataStream):
        self.wrapped = wrapped


class EncryptionDecorator(StreamDecorator):
    def __init__(self, wrapped: DataStream, key: int):
        super().__init__(wrapped)
        self.key = key

    def _xor(self, data: str) -> str:
        return "".join(chr(ord(ch) ^ self.key) for ch in data)

    def write(self, data: str) -> None:
        self.wrapped.write(self._xor(data))

    def read(self) -> str:
        return self._xor(self.wrapped.read())


class CompressionDecorator(StreamDecorator):
    def write(self, data: str) -> None:
        compressed = base64.b64encode(data.encode()).decode()
        self.wrapped.write(compressed)

    def read(self) -> str:
        return base64.b64decode(self.wrapped.read().encode()).decode()


class BufferedDecorator(StreamDecorator):
    def __init__(self, wrapped: DataStream):
        super().__init__(wrapped)
        self.buffer = ""

    def write(self, data: str) -> None:
        self.buffer += data

    def flush(self) -> None:
        self.wrapped.write(self.buffer)
        self.buffer = ""

    def read(self) -> str:
        return self.wrapped.read()


# Task 4
@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


class Validator(ABC):
    @abstractmethod
    def validate(self, value: str) -> ValidationResult:
        pass


class BaseValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        return ValidationResult()


class ValidatorDecorator(Validator):
    def __init__(self, wrapped: Validator):
        self.wrapped = wrapped

    def validate(self, value: str) -> ValidationResult:
        return self.wrapped.validate(value)


class RequiredDecorator(ValidatorDecorator):
    def validate(self, value: str) -> ValidationResult:
        result = self.wrapped.validate(value)
        if not value:
            result.errors.append("Поле обязательно")
        return result


class MinLengthDecorator(ValidatorDecorator):
    def __init__(self, wrapped: Validator, min_length: int):
        super().__init__(wrapped)
        self.min_length = min_length

    def validate(self, value: str) -> ValidationResult:
        result = self.wrapped.validate(value)
        if value and len(value) < self.min_length:
            result.errors.append(f"Минимальная длина: {self.min_length}")
        return result


class MaxLengthDecorator(ValidatorDecorator):
    def __init__(self, wrapped: Validator, max_length: int):
        super().__init__(wrapped)
        self.max_length = max_length

    def validate(self, value: str) -> ValidationResult:
        result = self.wrapped.validate(value)
        if len(value) > self.max_length:
            result.errors.append(f"Максимальная длина: {self.max_length}")
        return result


class RegexDecorator(ValidatorDecorator):
    def __init__(self, wrapped: Validator, predicate: Callable[[str], bool], message: str):
        super().__init__(wrapped)
        self.predicate = predicate
        self.message = message

    def validate(self, value: str) -> ValidationResult:
        result = self.wrapped.validate(value)
        if value and not self.predicate(value):
            result.errors.append(self.message)
        return result


class EmailDecorator(ValidatorDecorator):
    def validate(self, value: str) -> ValidationResult:
        result = self.wrapped.validate(value)
        if value and ("@" not in value or "." not in value.split("@")[-1]):
            result.errors.append("Некорректный email")
        return result


# Task 5
class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> dict | None:
        pass

    @abstractmethod
    def find_all(self) -> list[dict]:
        pass

    @abstractmethod
    def save(self, user: dict) -> None:
        pass


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {1: {"id": 1, "name": "Анна"}, 2: {"id": 2, "name": "Иван"}}

    def find_by_id(self, user_id: int) -> dict | None:
        return self.users.get(user_id)

    def find_all(self) -> list[dict]:
        return list(self.users.values())

    def save(self, user: dict) -> None:
        self.users[user["id"]] = user


class RepositoryDecorator(UserRepository):
    def __init__(self, wrapped: UserRepository):
        self.wrapped = wrapped

    def find_by_id(self, user_id: int) -> dict | None:
        return self.wrapped.find_by_id(user_id)

    def find_all(self) -> list[dict]:
        return self.wrapped.find_all()

    def save(self, user: dict) -> None:
        self.wrapped.save(user)


class CachingRepository(RepositoryDecorator):
    def __init__(self, wrapped: UserRepository):
        super().__init__(wrapped)
        self.cache: dict[int, dict] = {}

    def find_by_id(self, user_id: int) -> dict | None:
        if user_id not in self.cache:
            user = self.wrapped.find_by_id(user_id)
            if user is not None:
                self.cache[user_id] = user
        return self.cache.get(user_id)


class LoggingRepository(RepositoryDecorator):
    def _measure(self, action: Callable[[], object], label: str):
        start = time.perf_counter()
        result = action()
        duration = time.perf_counter() - start
        print(f"{label}: {duration:.6f}s")
        return result

    def find_by_id(self, user_id: int) -> dict | None:
        return self._measure(lambda: self.wrapped.find_by_id(user_id), f"find_by_id({user_id})")

    def find_all(self) -> list[dict]:
        return self._measure(self.wrapped.find_all, "find_all()")

    def save(self, user: dict) -> None:
        self._measure(lambda: self.wrapped.save(user), f"save({user['id']})")


class ReadOnlyRepository(RepositoryDecorator):
    def save(self, user: dict) -> None:
        raise PermissionError("Репозиторий только для чтения")


if __name__ == "__main__":
    print("Task 1")
    message = LengthLimitDecorator(
        UpperCaseDecorator(CensorDecorator(TrimDecorator(PlainTextMessage("  bad word text  ")), ["bad"])),
        12,
    )
    print(message.get_content())
    print("-" * 40)

    print("Task 2")
    client: HttpClient = CachingDecorator(LoggingDecorator(RetryDecorator(AuthDecorator(SimpleHttpClient(), "token"), 2)))
    print(client.send(Request("GET", "https://api.example.com/retry")))
    print(client.send(Request("GET", "https://api.example.com/retry")))
    print("-" * 40)

    print("Task 3")
    stream = MemoryStream()
    buffered = BufferedDecorator(stream)
    encrypted = EncryptionDecorator(buffered, 3)
    encrypted.write("secret")
    buffered.flush()
    print(encrypted.read())
    print("-" * 40)

    print("Task 4")
    validator = EmailDecorator(
        MinLengthDecorator(
            MaxLengthDecorator(RequiredDecorator(BaseValidator()), 30),
            5,
        )
    )
    print(validator.validate("bad"))
    print(validator.validate("user@example.com"))
    print("-" * 40)

    print("Task 5")
    repository: UserRepository = ReadOnlyRepository(LoggingRepository(CachingRepository(InMemoryUserRepository())))
    print(repository.find_by_id(1))
    print(repository.find_all())
    try:
        repository.save({"id": 3, "name": "Мария"})
    except PermissionError as error:
        print(error)

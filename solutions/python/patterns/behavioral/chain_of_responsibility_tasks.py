from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Handler(ABC):
    def __init__(self):
        self.next_handler: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        self.next_handler = handler
        return handler

    def pass_next(self, payload):
        if self.next_handler is None:
            return None
        return self.next_handler.handle(payload)

    @abstractmethod
    def handle(self, payload):
        pass


# Task 1
@dataclass
class HttpRequest:
    headers: dict[str, str]
    body: dict[str, str]


class AuthMiddleware(Handler):
    def handle(self, payload: HttpRequest):
        if payload.headers.get("Authorization") != "valid-token":
            return "401 Unauthorized"
        return self.pass_next(payload)


class RateLimitMiddleware(Handler):
    def __init__(self, limit: int):
        super().__init__()
        self.limit = limit
        self.counter: dict[str, int] = {}

    def handle(self, payload: HttpRequest):
        token = payload.headers["Authorization"]
        self.counter[token] = self.counter.get(token, 0) + 1
        if self.counter[token] > self.limit:
            return "429 Too Many Requests"
        return self.pass_next(payload)


class ValidationMiddleware(Handler):
    def __init__(self, required_fields: list[str]):
        super().__init__()
        self.required_fields = required_fields

    def handle(self, payload: HttpRequest):
        missing = [field for field in self.required_fields if field not in payload.body]
        if missing:
            return f"400 Missing fields: {missing}"
        return self.pass_next(payload)


class HandlerMiddleware(Handler):
    def handle(self, payload: HttpRequest):
        return f"200 OK: {payload.body}"


# Task 2
class RegistrationValidator(Handler):
    def pass_or_error(self, value: str):
        return self.pass_next(value)


class NotEmptyValidator(RegistrationValidator):
    def handle(self, payload: str):
        if not payload:
            return "Поле пустое"
        return self.pass_or_error(payload)


class MinLengthValidator(RegistrationValidator):
    def __init__(self, min_length: int):
        super().__init__()
        self.min_length = min_length

    def handle(self, payload: str):
        if len(payload) < self.min_length:
            return f"Минимальная длина {self.min_length}"
        return self.pass_or_error(payload)


class MaxLengthValidator(RegistrationValidator):
    def __init__(self, max_length: int):
        super().__init__()
        self.max_length = max_length

    def handle(self, payload: str):
        if len(payload) > self.max_length:
            return f"Максимальная длина {self.max_length}"
        return self.pass_or_error(payload)


class RegexValidator(RegistrationValidator):
    def __init__(self, predicate, message: str):
        super().__init__()
        self.predicate = predicate
        self.message = message

    def handle(self, payload: str):
        if not self.predicate(payload):
            return self.message
        return self.pass_or_error(payload)


class UniqueEmailValidator(RegistrationValidator):
    def __init__(self, used_emails: set[str]):
        super().__init__()
        self.used_emails = used_emails

    def handle(self, payload: str):
        if payload in self.used_emails:
            return "Email уже занят"
        return self.pass_or_error(payload)


class OkValidator(RegistrationValidator):
    def handle(self, payload: str):
        return "OK"


# Task 3
@dataclass
class CreditRequest:
    applicant: str
    amount: int


class CreditApprover(Handler):
    def __init__(self, limit: int, title: str):
        super().__init__()
        self.limit = limit
        self.title = title

    def handle(self, payload: CreditRequest):
        if payload.amount <= self.limit:
            return f"{self.title} одобрил заявку на {payload.amount}"
        return self.pass_next(payload)


class BoardApprover(Handler):
    def handle(self, payload: CreditRequest):
        return f"Совет директоров рассматривает заявку на {payload.amount}"


# Task 4
@dataclass
class SupportTicket:
    title: str
    category: str
    priority: str


class SupportLevel(Handler):
    def __init__(self, name: str, categories: set[str], priorities: set[str]):
        super().__init__()
        self.name = name
        self.categories = categories
        self.priorities = priorities

    def handle(self, payload: SupportTicket):
        if payload.category in self.categories or payload.priority in self.priorities:
            return f"{self.name} обработал тикет '{payload.title}'"
        return self.pass_next(payload)


class DeveloperSupport(Handler):
    def handle(self, payload: SupportTicket):
        return f"DeveloperSupport обработал критический тикет '{payload.title}'"


# Task 5
@dataclass
class ImageContext:
    width: int
    height: int
    format: str
    has_watermark: bool = False
    compressed: bool = False
    operations: list[str] = field(default_factory=list)


class ImageFilter(Handler):
    def pass_forward(self, payload: ImageContext):
        return self.pass_next(payload) or payload


class ResizeFilter(ImageFilter):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height

    def handle(self, payload: ImageContext):
        payload.width = self.width
        payload.height = self.height
        payload.operations.append(f"resize:{self.width}x{self.height}")
        return self.pass_forward(payload)


class WatermarkFilter(ImageFilter):
    def handle(self, payload: ImageContext):
        payload.has_watermark = True
        payload.operations.append("watermark")
        return self.pass_forward(payload)


class CompressionFilter(ImageFilter):
    def handle(self, payload: ImageContext):
        payload.compressed = True
        payload.operations.append("compress")
        return self.pass_forward(payload)


class FormatConversionFilter(ImageFilter):
    def __init__(self, target_format: str):
        super().__init__()
        self.target_format = target_format

    def handle(self, payload: ImageContext):
        payload.format = self.target_format
        payload.operations.append(f"convert:{self.target_format}")
        return self.pass_forward(payload)


if __name__ == "__main__":
    print("Task 1")
    auth = AuthMiddleware()
    rate = RateLimitMiddleware(2)
    validation = ValidationMiddleware(["title", "text"])
    final = HandlerMiddleware()
    auth.set_next(rate).set_next(validation).set_next(final)
    request = HttpRequest({"Authorization": "valid-token"}, {"title": "Hi", "text": "Hello"})
    print(auth.handle(request))
    print(auth.handle(request))
    print(auth.handle(request))
    print("-" * 40)

    print("Task 2")
    username_chain = NotEmptyValidator()
    username_chain.set_next(MinLengthValidator(3)).set_next(MaxLengthValidator(12)).set_next(OkValidator())
    email_chain = NotEmptyValidator()
    email_chain.set_next(
        RegexValidator(lambda value: "@" in value, "Некорректный email")
    ).set_next(UniqueEmailValidator({"used@example.com"})).set_next(OkValidator())
    print(username_chain.handle("ab"))
    print(username_chain.handle("alexey"))
    print(email_chain.handle("used@example.com"))
    print(email_chain.handle("new@example.com"))
    print("-" * 40)

    print("Task 3")
    auto = CreditApprover(50_000, "Автомат")
    manager = CreditApprover(200_000, "Менеджер")
    director = CreditApprover(1_000_000, "Директор")
    board = BoardApprover()
    auto.set_next(manager).set_next(director).set_next(board)
    print(auto.handle(CreditRequest("Иван", 40_000)))
    print(auto.handle(CreditRequest("Анна", 300_000)))
    print(auto.handle(CreditRequest("ООО Ромашка", 2_000_000)))
    print("-" * 40)

    print("Task 4")
    l1 = SupportLevel("L1Support", {"faq"}, {"low"})
    l2 = SupportLevel("L2Support", {"technical"}, {"medium"})
    l3 = SupportLevel("L3Support", {"bug"}, {"high"})
    dev = DeveloperSupport()
    l1.set_next(l2).set_next(l3).set_next(dev)
    print(l1.handle(SupportTicket("Не входит", "technical", "medium")))
    print(l1.handle(SupportTicket("Падение продакшена", "critical", "critical")))
    print("-" * 40)

    print("Task 5")
    resize = ResizeFilter(400, 300)
    watermark = WatermarkFilter()
    compress = CompressionFilter()
    convert = FormatConversionFilter("webp")
    resize.set_next(watermark).set_next(compress).set_next(convert)
    image = ImageContext(1920, 1080, "png")
    print(resize.handle(image))

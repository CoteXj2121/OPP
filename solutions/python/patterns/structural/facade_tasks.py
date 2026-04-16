from __future__ import annotations

from dataclasses import dataclass


# Task 1
class InventoryService:
    def reserve(self, items: list[str]) -> str:
        return f"Зарезервированы товары: {items}"


class PaymentService:
    def charge(self, user_id: int, payment_method: str) -> str:
        return f"Платеж пользователя {user_id} через {payment_method} успешен"


class ShippingService:
    def create_delivery(self, items: list[str]) -> str:
        return f"Создана доставка для {len(items)} товаров"


class NotificationService:
    def send(self, user_id: int, text: str) -> str:
        return f"Уведомление пользователю {user_id}: {text}"


class OrderFacade:
    def __init__(self):
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()
        self.notification = NotificationService()

    def place_order(self, user_id: int, items: list[str], payment_method: str) -> list[str]:
        return [
            self.inventory.reserve(items),
            self.payment.charge(user_id, payment_method),
            self.shipping.create_delivery(items),
            self.notification.send(user_id, "Заказ оформлен"),
        ]


# Task 2
class UserRepository:
    def __init__(self):
        self.users: dict[str, dict] = {}

    def add(self, name: str, email: str, password_hash: str) -> None:
        self.users[email] = {"name": name, "email": email, "password_hash": password_hash}

    def get(self, email: str) -> dict | None:
        return self.users.get(email)


class PasswordHasher:
    def hash(self, password: str) -> str:
        return f"hash::{password}"

    def verify(self, password: str, stored_hash: str) -> bool:
        return self.hash(password) == stored_hash


class TokenService:
    def issue(self, email: str) -> str:
        return f"token::{email}"


class SessionStore:
    def __init__(self):
        self.sessions: set[str] = set()

    def save(self, token: str) -> None:
        self.sessions.add(token)

    def remove(self, token: str) -> None:
        self.sessions.discard(token)


class AuthFacade:
    def __init__(self):
        self.users = UserRepository()
        self.hasher = PasswordHasher()
        self.tokens = TokenService()
        self.sessions = SessionStore()

    def register(self, name: str, email: str, password: str) -> str:
        self.users.add(name, email, self.hasher.hash(password))
        return f"Пользователь {email} зарегистрирован"

    def login(self, email: str, password: str) -> str:
        user = self.users.get(email)
        if user is None or not self.hasher.verify(password, user["password_hash"]):
            return "Ошибка входа"
        token = self.tokens.issue(email)
        self.sessions.save(token)
        return token

    def logout(self, token: str) -> str:
        self.sessions.remove(token)
        return "Сессия завершена"


# Task 3
class DataQueryService:
    def query(self, report_type: str, filters: dict) -> list[dict]:
        return [{"report_type": report_type, "filters": filters}]


class ReportBuilder:
    def build(self, rows: list[dict]) -> dict:
        return {"rows": rows, "count": len(rows)}


class ChartGenerator:
    def build(self, report: dict) -> str:
        return f"chart({report['count']})"


class ExportService:
    def export(self, report: dict, chart: str, output_format: str) -> str:
        return f"{output_format.upper()}::{report}::{chart}"


class ReportFacade:
    def __init__(self):
        self.query_service = DataQueryService()
        self.builder = ReportBuilder()
        self.charts = ChartGenerator()
        self.exporter = ExportService()

    def generate(self, report_type: str, filters: dict, output_format: str) -> str:
        rows = self.query_service.query(report_type, filters)
        report = self.builder.build(rows)
        chart = self.charts.build(report)
        return self.exporter.export(report, chart, output_format)


# Task 4
class FileReader:
    def read(self, src: str) -> str:
        return f"binary({src})"


class CodecDetector:
    def detect(self, src: str) -> str:
        return "h264" if src.endswith(".mp4") else "mp3"


class VideoEncoder:
    def encode(self, data: str, codec: str, target_format: str) -> str:
        return f"video[{codec}->{target_format}]::{data}"


class AudioEncoder:
    def encode(self, data: str, codec: str, target_format: str) -> str:
        return f"audio[{codec}->{target_format}]::{data}"


class FileWriter:
    def write(self, data: str, target_format: str) -> str:
        return f"saved::{target_format}::{data}"


class MediaConverter:
    def __init__(self):
        self.reader = FileReader()
        self.detector = CodecDetector()
        self.video_encoder = VideoEncoder()
        self.audio_encoder = AudioEncoder()
        self.writer = FileWriter()

    def convert_video(self, src: str, target_format: str) -> str:
        data = self.reader.read(src)
        codec = self.detector.detect(src)
        encoded = self.video_encoder.encode(data, codec, target_format)
        return self.writer.write(encoded, target_format)

    def convert_audio(self, src: str, target_format: str) -> str:
        data = self.reader.read(src)
        codec = self.detector.detect(src)
        encoded = self.audio_encoder.encode(data, codec, target_format)
        return self.writer.write(encoded, target_format)


# Task 5
class LightingSystem:
    def on(self) -> str:
        return "Свет включен"

    def night(self) -> str:
        return "Ночной свет активирован"

    def off(self) -> str:
        return "Свет выключен"


class ClimateSystem:
    def comfort(self) -> str:
        return "Комфортная температура установлена"

    def eco(self) -> str:
        return "Экономичный режим климата"


class SecuritySystem:
    def disarm(self) -> str:
        return "Охрана снята"

    def arm(self) -> str:
        return "Охрана включена"


class EntertainmentSystem:
    def welcome(self) -> str:
        return "Музыка приветствия включена"

    def sleep(self) -> str:
        return "Техника переведена в тихий режим"

    def off(self) -> str:
        return "Развлечения выключены"


class SmartHomeFacade:
    def __init__(self):
        self.light = LightingSystem()
        self.climate = ClimateSystem()
        self.security = SecuritySystem()
        self.entertainment = EntertainmentSystem()

    def arrive_home(self) -> list[str]:
        return [
            self.security.disarm(),
            self.light.on(),
            self.climate.comfort(),
            self.entertainment.welcome(),
        ]

    def leave_home(self) -> list[str]:
        return [
            self.entertainment.off(),
            self.light.off(),
            self.climate.eco(),
            self.security.arm(),
        ]

    def night_mode(self) -> list[str]:
        return [
            self.light.night(),
            self.climate.eco(),
            self.entertainment.sleep(),
            self.security.arm(),
        ]


if __name__ == "__main__":
    print("Task 1")
    print(OrderFacade().place_order(1, ["Книга", "Ручка"], "card"))
    print("-" * 40)

    print("Task 2")
    auth = AuthFacade()
    print(auth.register("Иван", "ivan@example.com", "secret"))
    token = auth.login("ivan@example.com", "secret")
    print(token)
    print(auth.logout(token))
    print("-" * 40)

    print("Task 3")
    print(ReportFacade().generate("sales", {"region": "RU"}, "pdf"))
    print("-" * 40)

    print("Task 4")
    converter = MediaConverter()
    print(converter.convert_video("movie.mp4", "avi"))
    print(converter.convert_audio("song.mp3", "wav"))
    print("-" * 40)

    print("Task 5")
    home = SmartHomeFacade()
    print(home.arrive_home())
    print(home.leave_home())
    print(home.night_mode())

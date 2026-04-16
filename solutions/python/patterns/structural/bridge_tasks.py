from __future__ import annotations

from abc import ABC, abstractmethod


# Task 1
class Renderer(ABC):
    @abstractmethod
    def render(self, shape_name: str, data: str) -> str:
        pass


class RasterRenderer(Renderer):
    def render(self, shape_name: str, data: str) -> str:
        return f"Raster render {shape_name}: {data}"


class VectorRenderer(Renderer):
    def render(self, shape_name: str, data: str) -> str:
        return f"Vector render {shape_name}: {data}"


class Shape(ABC):
    def __init__(self, renderer: Renderer):
        self.renderer = renderer

    @abstractmethod
    def draw(self) -> str:
        pass


class Circle(Shape):
    def __init__(self, renderer: Renderer, radius: float):
        super().__init__(renderer)
        self.radius = radius

    def draw(self) -> str:
        return self.renderer.render("Circle", f"radius={self.radius}")


class Rectangle(Shape):
    def __init__(self, renderer: Renderer, width: float, height: float):
        super().__init__(renderer)
        self.width = width
        self.height = height

    def draw(self) -> str:
        return self.renderer.render("Rectangle", f"{self.width}x{self.height}")


class Triangle(Shape):
    def __init__(self, renderer: Renderer, a: float, b: float, c: float):
        super().__init__(renderer)
        self.a = a
        self.b = b
        self.c = c

    def draw(self) -> str:
        return self.renderer.render("Triangle", f"sides={self.a},{self.b},{self.c}")


# Task 2
class Device(ABC):
    @abstractmethod
    def toggle_power(self) -> None:
        pass

    @abstractmethod
    def volume_up(self) -> None:
        pass

    @abstractmethod
    def mute(self) -> None:
        pass


class TV(Device):
    def __init__(self):
        self.power = False
        self.volume = 10

    def toggle_power(self) -> None:
        self.power = not self.power
        print(f"TV power: {self.power}")

    def volume_up(self) -> None:
        self.volume += 1
        print(f"TV volume: {self.volume}")

    def mute(self) -> None:
        self.volume = 0
        print("TV muted")


class Radio(Device):
    def __init__(self):
        self.power = False
        self.volume = 5

    def toggle_power(self) -> None:
        self.power = not self.power
        print(f"Radio power: {self.power}")

    def volume_up(self) -> None:
        self.volume += 1
        print(f"Radio volume: {self.volume}")

    def mute(self) -> None:
        self.volume = 0
        print("Radio muted")


class Remote:
    def __init__(self, device: Device):
        self.device = device

    def power(self) -> None:
        self.device.toggle_power()

    def volume_up(self) -> None:
        self.device.volume_up()


class AdvancedRemote(Remote):
    def mute(self) -> None:
        self.device.mute()


# Task 3
class MessageSender(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass


class EmailSender(MessageSender):
    def send(self, message: str) -> str:
        return f"Email: {message}"


class SmsSender(MessageSender):
    def send(self, message: str) -> str:
        return f"SMS: {message}"


class TelegramSender(MessageSender):
    def send(self, message: str) -> str:
        return f"Telegram: {message}"


class Notification(ABC):
    def __init__(self, sender: MessageSender):
        self.sender = sender

    @abstractmethod
    def send(self, text: str) -> str:
        pass


class RegularNotification(Notification):
    def send(self, text: str) -> str:
        return self.sender.send(f"[обычное] {text}")


class UrgentNotification(Notification):
    def send(self, text: str) -> str:
        return self.sender.send(f"[СРОЧНО] {text.upper()}")


class ScheduledNotification(Notification):
    def send(self, text: str) -> str:
        return self.sender.send(f"[запланировано] {text}")


# Task 4
class Exporter(ABC):
    @abstractmethod
    def export(self, title: str, data: dict) -> str:
        pass


class PdfExporter(Exporter):
    def export(self, title: str, data: dict) -> str:
        return f"[PDF] {title}: {data}"


class ExcelExporter(Exporter):
    def export(self, title: str, data: dict) -> str:
        return f"[Excel] {title}: {data}"


class CsvExporter(Exporter):
    def export(self, title: str, data: dict) -> str:
        return f"[CSV] {title}: {data}"


class Report(ABC):
    def __init__(self, exporter: Exporter):
        self.exporter = exporter

    @abstractmethod
    def generate_data(self) -> dict:
        pass

    def export(self) -> str:
        return self.exporter.export(self.__class__.__name__, self.generate_data())


class FinancialReport(Report):
    def generate_data(self) -> dict:
        return {"income": 150000, "expense": 90000}


class StatisticalReport(Report):
    def generate_data(self) -> dict:
        return {"users": 1200, "sessions": 3400}


class AuditReport(Report):
    def generate_data(self) -> dict:
        return {"checks": 18, "violations": 2}


# Task 5
class AnimationRenderer(ABC):
    @abstractmethod
    def render_animation(self, character_type: str, animation: str) -> str:
        pass


class OpenGLRenderer(AnimationRenderer):
    def render_animation(self, character_type: str, animation: str) -> str:
        return f"OpenGL: {character_type} -> {animation}"


class VulkanRenderer(AnimationRenderer):
    def render_animation(self, character_type: str, animation: str) -> str:
        return f"Vulkan: {character_type} -> {animation}"


class Character(ABC):
    def __init__(self, renderer: AnimationRenderer):
        self.renderer = renderer

    @abstractmethod
    def attack(self) -> str:
        pass


class Warrior(Character):
    def attack(self) -> str:
        return self.renderer.render_animation("Warrior", "Slash")


class Mage(Character):
    def attack(self) -> str:
        return self.renderer.render_animation("Mage", "Fireball")


class Archer(Character):
    def attack(self) -> str:
        return self.renderer.render_animation("Archer", "Arrow Shot")


class Rogue(Character):
    def attack(self) -> str:
        return self.renderer.render_animation("Rogue", "Backstab")


if __name__ == "__main__":
    print("Task 1")
    print(Circle(RasterRenderer(), 5).draw())
    print(Rectangle(VectorRenderer(), 4, 6).draw())
    print(Triangle(RasterRenderer(), 3, 4, 5).draw())
    print("-" * 40)

    print("Task 2")
    remote = AdvancedRemote(TV())
    remote.power()
    remote.volume_up()
    remote.mute()
    print("-" * 40)

    print("Task 3")
    print(RegularNotification(EmailSender()).send("Заказ принят"))
    print(UrgentNotification(SmsSender()).send("Подтвердите вход"))
    print(ScheduledNotification(TelegramSender()).send("Встреча в 18:00"))
    print("-" * 40)

    print("Task 4")
    print(FinancialReport(PdfExporter()).export())
    print(StatisticalReport(ExcelExporter()).export())
    print(AuditReport(CsvExporter()).export())
    print("-" * 40)

    print("Task 5")
    print(Warrior(OpenGLRenderer()).attack())
    print(Mage(VulkanRenderer()).attack())
    print(Rogue(OpenGLRenderer()).attack())

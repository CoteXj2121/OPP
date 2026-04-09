from __future__ import annotations

from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass


class EmailNotification(Notification):
    def __init__(self, address: str):
        self.address = address

    def send(self, message: str) -> str:
        return f"Email -> {self.address}: {message}"


class SmsNotification(Notification):
    def __init__(self, phone: str):
        self.phone = phone

    def send(self, message: str) -> str:
        return f"SMS -> {self.phone}: {message}"


class PushNotification(Notification):
    def __init__(self, device_token: str):
        self.device_token = device_token

    def send(self, message: str) -> str:
        return f"Push -> {self.device_token}: {message}"


class Notifier(ABC):
    def __init__(self, target: str):
        self.target = target

    @abstractmethod
    def create_notification(self) -> Notification:
        pass

    def notify(self, message: str) -> str:
        notification = self.create_notification()
        return notification.send(message)


class EmailNotifier(Notifier):
    def create_notification(self) -> Notification:
        return EmailNotification(self.target)


class SmsNotifier(Notifier):
    def create_notification(self) -> Notification:
        return SmsNotification(self.target)


class PushNotifier(Notifier):
    def create_notification(self) -> Notification:
        return PushNotification(self.target)


if __name__ == "__main__":
    email_notifier = EmailNotifier("user@example.com")
    sms_notifier = SmsNotifier("+79001234567")
    push_notifier = PushNotifier("device-123")

    print(email_notifier.notify("Ваш заказ подтверждён"))
    print(sms_notifier.notify("Код подтверждения: 1234"))
    print(push_notifier.notify("У вас новое сообщение"))

from abc import ABC, abstractmethod


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass


class EmailChannel(NotificationChannel):
    def send(self, recipient: str, message: str) -> None:
        print(f"Email: {recipient} - {message}")


class SmsChannel(NotificationChannel):
    def send(self, recipient: str, message: str) -> None:
        print(f"SMS: {recipient} - {message}")


class PushChannel(NotificationChannel):
    def send(self, recipient: str, message: str) -> None:
        print(f"Push: {recipient} - {message}")


class NotificationService:
    def __init__(self, channel: NotificationChannel):
        self.channel = channel

    def send(self, recipient: str, message: str) -> None:
        self.channel.send(recipient, message)


if __name__ == "__main__":
    email_service = NotificationService(EmailChannel())
    sms_service = NotificationService(SmsChannel())
    push_service = NotificationService(PushChannel())

    email_service.send("user@example.com", "Ваш заказ подтвержден")
    sms_service.send("+79001234567", "Код подтверждения: 1234")
    push_service.send("device-123", "У вас новое уведомление")

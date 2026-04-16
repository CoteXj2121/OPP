from abc import ABC, abstractmethod


class NotificationSender(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass


class EmailSender(NotificationSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"Email: {recipient} - {message}")


class SmsSender(NotificationSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"SMS: {recipient} - {message}")


class OrderService:
    def __init__(self, notifier: NotificationSender):
        self.notifier = notifier

    def place_order(self, order_id: int, contact: str) -> None:
        print(f"Заказ #{order_id} оформлен")
        self.notifier.send(contact, f"Ваш заказ #{order_id} принят")


if __name__ == "__main__":
    email_service = OrderService(EmailSender())
    sms_service = OrderService(SmsSender())

    email_service.place_order(101, "user@example.com")
    sms_service.place_order(102, "+79001234567")

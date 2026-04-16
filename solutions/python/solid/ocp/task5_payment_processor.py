from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


class CardPayment(PaymentMethod):
    def pay(self, amount: float) -> None:
        print(f"Оплата картой: {amount} руб.")


class CryptoPayment(PaymentMethod):
    def pay(self, amount: float) -> None:
        print(f"Оплата криптовалютой: {amount} руб.")


class SBPPayment(PaymentMethod):
    def pay(self, amount: float) -> None:
        print(f"Оплата через СБП: {amount} руб.")


class PaymentProcessor:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method

    def pay(self, amount: float) -> None:
        self.payment_method.pay(amount)


if __name__ == "__main__":
    PaymentProcessor(CardPayment()).pay(1500.0)
    PaymentProcessor(CryptoPayment()).pay(3200.0)
    PaymentProcessor(SBPPayment()).pay(2100.0)

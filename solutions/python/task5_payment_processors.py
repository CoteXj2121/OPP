from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount: float, currency: str) -> str:
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> str:
        pass


class StripeGateway(PaymentGateway):
    def pay(self, amount: float, currency: str) -> str:
        return f"Stripe: списано {amount} {currency}"

    def refund(self, transaction_id: str) -> str:
        return f"Stripe: возврат по транзакции {transaction_id}"


class PayPalGateway(PaymentGateway):
    def pay(self, amount: float, currency: str) -> str:
        return f"PayPal: списано {amount} {currency}"

    def refund(self, transaction_id: str) -> str:
        return f"PayPal: возврат по транзакции {transaction_id}"


class YookassaGateway(PaymentGateway):
    def pay(self, amount: float, currency: str) -> str:
        return f"ЮKassa: списано {amount} {currency}"

    def refund(self, transaction_id: str) -> str:
        return f"ЮKassa: возврат по транзакции {transaction_id}"


class PaymentProcessor(ABC):
    @abstractmethod
    def create_gateway(self) -> PaymentGateway:
        pass

    def checkout(self, amount: float, currency: str = "RUB") -> str:
        gateway = self.create_gateway()
        return gateway.pay(amount, currency)


class StripeProcessor(PaymentProcessor):
    def create_gateway(self) -> PaymentGateway:
        return StripeGateway()


class PayPalProcessor(PaymentProcessor):
    def create_gateway(self) -> PaymentGateway:
        return PayPalGateway()


class YookassaProcessor(PaymentProcessor):
    def create_gateway(self) -> PaymentGateway:
        return YookassaGateway()


if __name__ == "__main__":
    print(StripeProcessor().checkout(4990.0))
    print(PayPalProcessor().checkout(4990.0, "USD"))
    print(YookassaProcessor().checkout(4990.0))

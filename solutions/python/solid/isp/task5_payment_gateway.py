from abc import ABC, abstractmethod


class Chargeable(ABC):
    @abstractmethod
    def charge(self, amount: float) -> None:
        pass


class Refundable(ABC):
    @abstractmethod
    def refund(self, transaction_id: str) -> None:
        pass


class HistoryProvider(ABC):
    @abstractmethod
    def get_transaction_history(self) -> list[dict]:
        pass


class Reportable(ABC):
    @abstractmethod
    def generate_report(self) -> str:
        pass


class FullGateway(Chargeable, Refundable, HistoryProvider, Reportable):
    def charge(self, amount: float) -> None:
        print(f"Списание: {amount} руб.")

    def refund(self, transaction_id: str) -> None:
        print(f"Возврат по транзакции {transaction_id}")

    def get_transaction_history(self) -> list[dict]:
        return [{"id": "tx1", "amount": 500}]

    def generate_report(self) -> str:
        return "Отчет: транзакций - 1"


class BasicGateway(Chargeable):
    def charge(self, amount: float) -> None:
        print(f"Списание: {amount} руб.")


if __name__ == "__main__":
    basic_gateway = BasicGateway()
    basic_gateway.charge(1500.0)

    full_gateway = FullGateway()
    full_gateway.refund("tx123")
    print(full_gateway.get_transaction_history())
    print(full_gateway.generate_report())

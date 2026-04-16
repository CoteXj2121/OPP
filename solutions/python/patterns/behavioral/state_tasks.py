from __future__ import annotations

from abc import ABC, abstractmethod


# Task 1
class TrafficLightState(ABC):
    name = ""
    duration = 0

    @abstractmethod
    def next_state(self) -> "TrafficLightState":
        pass


class RedState(TrafficLightState):
    name = "Red"
    duration = 60

    def next_state(self) -> TrafficLightState:
        return GreenState()


class YellowState(TrafficLightState):
    name = "Yellow"
    duration = 5

    def next_state(self) -> TrafficLightState:
        return RedState()


class GreenState(TrafficLightState):
    name = "Green"
    duration = 45

    def next_state(self) -> TrafficLightState:
        return YellowState()


class TrafficLight:
    def __init__(self):
        self.state: TrafficLightState = RedState()

    def switch(self) -> tuple[str, int]:
        current = (self.state.name, self.state.duration)
        self.state = self.state.next_state()
        return current


# Task 2
class OrderState(ABC):
    name = ""

    def pay(self):
        raise RuntimeError("Операция недоступна")

    def ship(self):
        raise RuntimeError("Операция недоступна")

    def deliver(self):
        raise RuntimeError("Операция недоступна")

    def complete(self):
        raise RuntimeError("Операция недоступна")

    def cancel(self):
        raise RuntimeError("Операция недоступна")


class NewOrderState(OrderState):
    name = "New"

    def pay(self):
        return PaidOrderState()

    def cancel(self):
        return CancelledOrderState()


class PaidOrderState(OrderState):
    name = "Paid"

    def ship(self):
        return ShippedOrderState()

    def cancel(self):
        return CancelledOrderState()


class ShippedOrderState(OrderState):
    name = "Shipped"

    def deliver(self):
        return DeliveredOrderState()

    def cancel(self):
        return CancelledOrderState()


class DeliveredOrderState(OrderState):
    name = "Delivered"

    def complete(self):
        return CompletedOrderState()


class CompletedOrderState(OrderState):
    name = "Completed"


class CancelledOrderState(OrderState):
    name = "Cancelled"


class Order:
    def __init__(self):
        self.state: OrderState = NewOrderState()

    def transition(self, action: str) -> str:
        self.state = getattr(self.state, action)()
        return self.state.name


# Task 3
class ATMState(ABC):
    def insert_card(self, atm: "ATM"):
        raise RuntimeError("Недоступно")

    def enter_pin(self, atm: "ATM", pin: str):
        raise RuntimeError("Недоступно")

    def withdraw(self, atm: "ATM", amount: int):
        raise RuntimeError("Недоступно")


class IdleState(ATMState):
    def insert_card(self, atm: "ATM"):
        atm.state = CardInsertedState()
        return "Карта вставлена"


class CardInsertedState(ATMState):
    def enter_pin(self, atm: "ATM", pin: str):
        if pin == atm.correct_pin:
            atm.pin_attempts = 0
            atm.state = AuthenticatedState()
            return "PIN верный"
        atm.pin_attempts += 1
        if atm.pin_attempts >= 3:
            atm.state = CardBlockedState()
            return "Карта заблокирована"
        return "PIN неверный"


class AuthenticatedState(ATMState):
    def withdraw(self, atm: "ATM", amount: int):
        atm.state = DispensingCashState()
        return f"Выдача {amount}"


class DispensingCashState(ATMState):
    def withdraw(self, atm: "ATM", amount: int):
        atm.state = IdleState()
        return "Операция завершена"


class CardBlockedState(ATMState):
    pass


class ATM:
    def __init__(self, correct_pin: str):
        self.correct_pin = correct_pin
        self.pin_attempts = 0
        self.state: ATMState = IdleState()


# Task 4
class TcpState(ABC):
    def open(self):
        raise RuntimeError("Недоступно")

    def syn(self):
        raise RuntimeError("Недоступно")

    def ack(self):
        raise RuntimeError("Недоступно")

    def close(self):
        raise RuntimeError("Недоступно")

    def send_data(self, data: str):
        raise RuntimeError("Недоступно")


class ClosedState(TcpState):
    def open(self):
        return ListenState()


class ListenState(TcpState):
    def syn(self):
        return SynReceivedState()


class SynReceivedState(TcpState):
    def ack(self):
        return EstablishedState()


class EstablishedState(TcpState):
    def close(self):
        return ClosedState()

    def send_data(self, data: str):
        return f"Sent: {data}"


class TcpConnection:
    def __init__(self):
        self.state: TcpState = ClosedState()

    def transition(self, action: str, *args):
        result = getattr(self.state, action)(*args)
        if isinstance(result, TcpState):
            self.state = result
            return self.state.__class__.__name__
        return result


# Task 5
class VendingState(ABC):
    def insert_coin(self, machine: "VendingMachine", value: int):
        raise RuntimeError("Недоступно")

    def select_product(self, machine: "VendingMachine", name: str):
        raise RuntimeError("Недоступно")

    def refund(self, machine: "VendingMachine"):
        raise RuntimeError("Недоступно")


class IdleVendingState(VendingState):
    def insert_coin(self, machine: "VendingMachine", value: int):
        machine.balance += value
        machine.state = HasMoneyState()
        return machine.balance


class HasMoneyState(VendingState):
    def insert_coin(self, machine: "VendingMachine", value: int):
        machine.balance += value
        return machine.balance

    def select_product(self, machine: "VendingMachine", name: str):
        if machine.stock.get(name, 0) == 0:
            machine.state = OutOfStockState()
            return "Нет товара"
        price = machine.prices[name]
        if machine.balance < price:
            return f"Недостаточно денег, нужно еще {price - machine.balance}"
        machine.stock[name] -= 1
        change = machine.balance - price
        machine.balance = 0
        machine.state = IdleVendingState()
        return f"Выдан {name}, сдача {change}"

    def refund(self, machine: "VendingMachine"):
        returned = machine.balance
        machine.balance = 0
        machine.state = IdleVendingState()
        return returned


class OutOfStockState(VendingState):
    def refund(self, machine: "VendingMachine"):
        returned = machine.balance
        machine.balance = 0
        machine.state = IdleVendingState()
        return returned


class VendingMachine:
    def __init__(self):
        self.state: VendingState = IdleVendingState()
        self.balance = 0
        self.prices = {"cola": 50, "chips": 70}
        self.stock = {"cola": 1, "chips": 0}


if __name__ == "__main__":
    print("Task 1")
    light = TrafficLight()
    print(light.switch())
    print(light.switch())
    print(light.switch())
    print("-" * 40)

    print("Task 2")
    order = Order()
    print(order.transition("pay"))
    print(order.transition("ship"))
    print(order.transition("deliver"))
    print(order.transition("complete"))
    print("-" * 40)

    print("Task 3")
    atm = ATM("1234")
    print(atm.state.insert_card(atm))
    print(atm.state.enter_pin(atm, "0000"))
    print(atm.state.enter_pin(atm, "1234"))
    print(atm.state.withdraw(atm, 1000))
    print("-" * 40)

    print("Task 4")
    connection = TcpConnection()
    print(connection.transition("open"))
    print(connection.transition("syn"))
    print(connection.transition("ack"))
    print(connection.transition("send_data", "hello"))
    print(connection.transition("close"))
    print("-" * 40)

    print("Task 5")
    machine = VendingMachine()
    print(machine.state.insert_coin(machine, 20))
    print(machine.state.insert_coin(machine, 40))
    print(machine.state.select_product(machine, "cola"))
    print(machine.state.insert_coin(machine, 70))
    print(machine.state.select_product(machine, "chips"))
    print(machine.state.refund(machine))

from __future__ import annotations

from dataclasses import dataclass, field


# Task 1
class ChatRoom:
    def __init__(self):
        self.users: dict[str, User] = {}
        self.history: list[str] = []

    def register(self, user: "User") -> None:
        self.users[user.name] = user

    def send(self, sender: str, message: str, recipient: str | None = None) -> None:
        if recipient is None:
            text = f"{sender} -> all: {message}"
            self.history.append(text)
            for user in self.users.values():
                user.receive(text)
        else:
            text = f"{sender} -> {recipient}: {message}"
            self.history.append(text)
            self.users[recipient].receive(text)


class User:
    def __init__(self, name: str, room: ChatRoom):
        self.name = name
        self.room = room
        self.inbox: list[str] = []
        room.register(self)

    def send(self, message: str, recipient: str | None = None) -> None:
        self.room.send(self.name, message, recipient)

    def receive(self, message: str) -> None:
        self.inbox.append(message)


# Task 2
class ControlTower:
    def __init__(self, runways: int):
        self.runways = runways
        self.busy = 0

    def request_takeoff(self, plane: str) -> str:
        if self.busy >= self.runways:
            return f"{plane}: ожидание взлета"
        self.busy += 1
        return f"{plane}: взлет разрешен"

    def request_landing(self, plane: str) -> str:
        if self.busy >= self.runways:
            return f"{plane}: ожидание посадки"
        self.busy += 1
        return f"{plane}: посадка разрешена"

    def release_runway(self) -> None:
        if self.busy > 0:
            self.busy -= 1


# Task 3
class RegistrationMediator:
    def __init__(self):
        self.is_company = False
        self.country = "RU"
        self.inn_visible = False
        self.submit_enabled = False
        self.phone_mask = "+7"
        self.fields = {"name": "", "email": "", "phone": "", "inn": ""}

    def set_company(self, value: bool) -> None:
        self.is_company = value
        self.inn_visible = value
        self._recalculate()

    def set_country(self, country: str) -> None:
        self.country = country
        self.phone_mask = "+7" if country == "RU" else "+1"

    def update_field(self, field: str, value: str) -> None:
        self.fields[field] = value
        self._recalculate()

    def _recalculate(self) -> None:
        required = ["name", "email", "phone"]
        if self.is_company:
            required.append("inn")
        self.submit_enabled = all(self.fields[field] for field in required)


# Task 4
@dataclass
class Order:
    trader: str
    side: str
    price: float
    quantity: int


class Exchange:
    def __init__(self):
        self.buy_orders: list[Order] = []
        self.sell_orders: list[Order] = []

    def submit(self, order: Order) -> str:
        if order.side == "buy":
            self.buy_orders.append(order)
            self.buy_orders.sort(key=lambda item: item.price, reverse=True)
        else:
            self.sell_orders.append(order)
            self.sell_orders.sort(key=lambda item: item.price)
        return self.match()

    def match(self) -> str:
        if not self.buy_orders or not self.sell_orders:
            return "Ордер добавлен в стакан"
        best_buy = self.buy_orders[0]
        best_sell = self.sell_orders[0]
        if best_buy.price >= best_sell.price:
            self.buy_orders.pop(0)
            self.sell_orders.pop(0)
            return f"Сделка: {best_buy.trader} купил у {best_sell.trader} по {best_sell.price}"
        return "Совпадений нет"


# Task 5
class GameMediator:
    def __init__(self):
        self.hp = 100
        self.score = 0
        self.messages: list[str] = []

    def notify(self, event: str, value: int | None = None) -> None:
        if event == "player:damage":
            self.hp -= value or 0
            self.messages.append(f"UI: HP = {self.hp}")
            self.messages.append("Sound: hit.wav")
        elif event == "enemy:killed":
            self.score += value or 0
            self.messages.append(f"UI: score = {self.score}")
            if self.score >= 100:
                self.messages.append("Victory check: complete")
        elif event == "level:complete":
            self.messages.append("UI: show victory screen")


if __name__ == "__main__":
    print("Task 1")
    room = ChatRoom()
    anna = User("Анна", room)
    ivan = User("Иван", room)
    anna.send("Привет всем")
    anna.send("Личное сообщение", "Иван")
    print(room.history)
    print(ivan.inbox)
    print("-" * 40)

    print("Task 2")
    tower = ControlTower(runways=1)
    print(tower.request_takeoff("SU-100"))
    print(tower.request_landing("SU-200"))
    tower.release_runway()
    print(tower.request_landing("SU-200"))
    print("-" * 40)

    print("Task 3")
    mediator = RegistrationMediator()
    mediator.set_company(True)
    mediator.set_country("US")
    mediator.update_field("name", "ООО Тест")
    mediator.update_field("email", "test@example.com")
    mediator.update_field("phone", "+123")
    mediator.update_field("inn", "123456")
    print(mediator.phone_mask, mediator.inn_visible, mediator.submit_enabled)
    print("-" * 40)

    print("Task 4")
    exchange = Exchange()
    print(exchange.submit(Order("Buyer", "buy", 101, 10)))
    print(exchange.submit(Order("Seller", "sell", 99, 10)))
    print("-" * 40)

    print("Task 5")
    game = GameMediator()
    game.notify("player:damage", 15)
    game.notify("enemy:killed", 100)
    game.notify("level:complete")
    print(game.messages)

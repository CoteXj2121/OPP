from dataclasses import dataclass


@dataclass
class OrderItem:
    name: str
    price: float
    qty: int


class Order:
    def __init__(self):
        self.items: list[OrderItem] = []

    def add_item(self, name: str, price: float, qty: int) -> None:
        self.items.append(OrderItem(name, price, qty))

    def get_total(self) -> float:
        return sum(item.price * item.qty for item in self.items)


class OrderLogger:
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


if __name__ == "__main__":
    order = Order()
    logger = OrderLogger()

    order.add_item("Книга", 350.0, 2)
    logger.log("Добавлен товар: Книга, кол-во: 2")

    order.add_item("Ручка", 50.0, 5)
    logger.log("Добавлен товар: Ручка, кол-во: 5")

    total = order.get_total()
    logger.log(f"Подсчет итога: {total}")
    print(f"Итого: {total}")

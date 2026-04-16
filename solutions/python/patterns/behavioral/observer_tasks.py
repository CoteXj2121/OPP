from __future__ import annotations

from dataclasses import dataclass


# Task 1
class StoreSubscriber:
    def update(self, product: str, old_price: float, new_price: float) -> None:
        pass


class Store:
    def __init__(self):
        self.subscribers: list[StoreSubscriber] = []
        self.prices: dict[str, float] = {}

    def subscribe(self, subscriber: StoreSubscriber) -> None:
        self.subscribers.append(subscriber)

    def set_price(self, product: str, price: float) -> None:
        old_price = self.prices.get(product, price)
        self.prices[product] = price
        for subscriber in self.subscribers:
            subscriber.update(product, old_price, price)


class Buyer(StoreSubscriber):
    def __init__(self, desired_price: float):
        self.desired_price = desired_price
        self.messages: list[str] = []

    def update(self, product: str, old_price: float, new_price: float) -> None:
        if new_price <= self.desired_price:
            self.messages.append(f"{product} стоит {new_price}")


class Analyst(StoreSubscriber):
    def __init__(self):
        self.log: list[str] = []

    def update(self, product: str, old_price: float, new_price: float) -> None:
        self.log.append(f"{product}: {old_price} -> {new_price}")


class DiscountManager(StoreSubscriber):
    def __init__(self):
        self.actions: list[str] = []

    def update(self, product: str, old_price: float, new_price: float) -> None:
        if old_price > 0 and new_price > old_price * 1.1:
            self.actions.append(f"Нужна скидка на {product}")


# Task 2
class EventEmitter:
    def __init__(self):
        self.listeners: dict[str, list[tuple[callable, bool]]] = {}

    def on(self, event: str, callback) -> None:
        self.listeners.setdefault(event, []).append((callback, False))

    def once(self, event: str, callback) -> None:
        self.listeners.setdefault(event, []).append((callback, True))

    def off(self, event: str, callback) -> None:
        self.listeners[event] = [
            (registered, once) for registered, once in self.listeners.get(event, []) if registered != callback
        ]

    def emit(self, event: str, *args) -> None:
        to_remove = []
        for callback, once in self.listeners.get(event, []):
            callback(*args)
            if once:
                to_remove.append(callback)
        for callback in to_remove:
            self.off(event, callback)


# Task 3
class ReactiveProperty:
    def __init__(self, value=""):
        self._value = value
        self.subscribers: list[callable] = []

    def subscribe(self, callback) -> None:
        self.subscribers.append(callback)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        for subscriber in self.subscribers:
            subscriber(new_value)


class ReactiveModel:
    def __init__(self):
        self.username = ReactiveProperty()
        self.email = ReactiveProperty()
        self.password = ReactiveProperty()


class FormValidator:
    def __init__(self):
        self.errors: list[str] = []

    def validate(self, model: ReactiveModel) -> None:
        self.errors.clear()
        if len(model.username.value) < 3:
            self.errors.append("Короткий username")
        if "@" not in model.email.value:
            self.errors.append("Некорректный email")
        if len(model.password.value) < 6:
            self.errors.append("Слабый пароль")


class LivePreview:
    def __init__(self):
        self.text = ""

    def render(self, model: ReactiveModel) -> None:
        self.text = f"username={model.username.value}, email={model.email.value}"


# Task 4
class MetricsSubscriber:
    def update(self, metrics: dict[str, int]) -> None:
        pass


class ServerMonitor:
    def __init__(self):
        self.subscribers: list[MetricsSubscriber] = []

    def subscribe(self, subscriber: MetricsSubscriber) -> None:
        self.subscribers.append(subscriber)

    def collect(self, cpu: int, ram: int, disk: int) -> None:
        metrics = {"cpu": cpu, "ram": ram, "disk": disk}
        for subscriber in self.subscribers:
            subscriber.update(metrics)


class AlertSystem(MetricsSubscriber):
    def __init__(self, threshold: int):
        self.threshold = threshold
        self.alerts: list[str] = []

    def update(self, metrics: dict[str, int]) -> None:
        for key, value in metrics.items():
            if value > self.threshold:
                self.alerts.append(f"ALERT {key}: {value}")


class MetricsDashboard(MetricsSubscriber):
    def __init__(self, limit: int):
        self.limit = limit
        self.history: list[dict[str, int]] = []

    def update(self, metrics: dict[str, int]) -> None:
        self.history.append(dict(metrics))
        self.history = self.history[-self.limit :]


class AutoScaler(MetricsSubscriber):
    def __init__(self):
        self.instances = 1

    def update(self, metrics: dict[str, int]) -> None:
        if metrics["cpu"] > 80:
            self.instances += 1


# Task 5
class ObservableCollection:
    def __init__(self):
        self.items: list = []
        self.listeners: list[callable] = []

    def subscribe(self, callback) -> None:
        self.listeners.append(callback)

    def _notify(self, event: str, payload=None) -> None:
        for listener in self.listeners:
            listener(event, payload)

    def add(self, item) -> None:
        self.items.append(item)
        self._notify("item_added", item)

    def remove(self, item) -> None:
        self.items.remove(item)
        self._notify("item_removed", item)

    def change(self, index: int, item) -> None:
        self.items[index] = item
        self._notify("item_changed", item)

    def clear(self) -> None:
        self.items.clear()
        self._notify("collection_cleared")


class FilteredView:
    def __init__(self, collection: ObservableCollection, predicate):
        self.collection = collection
        self.predicate = predicate
        self.items: list = []
        collection.subscribe(self.update)
        self.rebuild()

    def rebuild(self) -> None:
        self.items = [item for item in self.collection.items if self.predicate(item)]

    def update(self, event: str, payload=None) -> None:
        self.rebuild()


if __name__ == "__main__":
    print("Task 1")
    store = Store()
    buyer = Buyer(90)
    analyst = Analyst()
    manager = DiscountManager()
    store.subscribe(buyer)
    store.subscribe(analyst)
    store.subscribe(manager)
    store.set_price("Ноутбук", 100)
    store.set_price("Ноутбук", 85)
    store.set_price("Ноутбук", 120)
    print(buyer.messages)
    print(analyst.log)
    print(manager.actions)
    print("-" * 40)

    print("Task 2")
    emitter = EventEmitter()
    events: list[str] = []
    emitter.on("login", lambda user: events.append(f"on:{user}"))
    emitter.once("login", lambda user: events.append(f"once:{user}"))
    emitter.emit("login", "Анна")
    emitter.emit("login", "Иван")
    print(events)
    print("-" * 40)

    print("Task 3")
    model = ReactiveModel()
    validator = FormValidator()
    preview = LivePreview()
    for prop in (model.username, model.email, model.password):
        prop.subscribe(lambda _value, m=model, v=validator: v.validate(m))
        prop.subscribe(lambda _value, m=model, p=preview: p.render(m))
    model.username.value = "alex"
    model.email.value = "alex@example.com"
    model.password.value = "secret1"
    print(validator.errors)
    print(preview.text)
    print("-" * 40)

    print("Task 4")
    monitor = ServerMonitor()
    alerts = AlertSystem(80)
    dashboard = MetricsDashboard(3)
    scaler = AutoScaler()
    monitor.subscribe(alerts)
    monitor.subscribe(dashboard)
    monitor.subscribe(scaler)
    monitor.collect(50, 40, 20)
    monitor.collect(95, 60, 70)
    print(alerts.alerts)
    print(dashboard.history)
    print(scaler.instances)
    print("-" * 40)

    print("Task 5")
    collection = ObservableCollection()
    view = FilteredView(collection, lambda item: item % 2 == 0)
    collection.add(1)
    collection.add(2)
    collection.add(4)
    collection.change(0, 6)
    print(collection.items)
    print(view.items)

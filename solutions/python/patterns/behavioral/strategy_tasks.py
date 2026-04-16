from __future__ import annotations

import json
import time
import xml.etree.ElementTree as et
from abc import ABC, abstractmethod


# Task 1
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        pass


class BubbleSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        result = data[:]
        for i in range(len(result)):
            for j in range(len(result) - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result


class QuickSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data[:]
        pivot = data[0]
        left = [item for item in data[1:] if item <= pivot]
        right = [item for item in data[1:] if item > pivot]
        return self.sort(left) + [pivot] + self.sort(right)


class MergeSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data[:]
        middle = len(data) // 2
        left = self.sort(data[:middle])
        right = self.sort(data[middle:])
        result = []
        while left and right:
            if left[0] < right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        return result + left + right


class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self.strategy = strategy

    def sort(self, data: list[int]) -> tuple[list[int], float]:
        start = time.perf_counter()
        result = self.strategy.sort(data)
        return result, time.perf_counter() - start


# Task 2
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float, quantity: int, loyalty_points: int) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float, quantity: int, loyalty_points: int) -> float:
        return total


class PercentDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, total: float, quantity: int, loyalty_points: int) -> float:
        return total * (1 - self.percent / 100)


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, total: float, quantity: int, loyalty_points: int) -> float:
        return max(0, total - self.amount)


class BulkDiscount(DiscountStrategy):
    def __init__(self, min_quantity: int, percent: float):
        self.min_quantity = min_quantity
        self.percent = percent

    def apply(self, total: float, quantity: int, loyalty_points: int) -> float:
        if quantity > self.min_quantity:
            return total * (1 - self.percent / 100)
        return total


class LoyaltyDiscount(DiscountStrategy):
    def apply(self, total: float, quantity: int, loyalty_points: int) -> float:
        return max(0, total - loyalty_points * 0.1)


class Cart:
    def __init__(self, total: float, quantity: int, loyalty_points: int):
        self.total = total
        self.quantity = quantity
        self.loyalty_points = loyalty_points

    def best_total(self, strategies: list[DiscountStrategy]) -> float:
        return min(strategy.apply(self.total, self.quantity, self.loyalty_points) for strategy in strategies)


# Task 3
class ExportStrategy(ABC):
    @abstractmethod
    def export(self, rows: list[dict]) -> str:
        pass


class CsvExporter(ExportStrategy):
    def export(self, rows: list[dict]) -> str:
        headers = list(rows[0].keys())
        lines = [",".join(headers)]
        for row in rows:
            lines.append(",".join(str(row[key]) for key in headers))
        return "\n".join(lines)


class JsonExporter(ExportStrategy):
    def export(self, rows: list[dict]) -> str:
        return json.dumps(rows, ensure_ascii=False)


class XmlExporter(ExportStrategy):
    def export(self, rows: list[dict]) -> str:
        root = et.Element("rows")
        for row in rows:
            item = et.SubElement(root, "row")
            for key, value in row.items():
                node = et.SubElement(item, key)
                node.text = str(value)
        return et.tostring(root, encoding="unicode")


class MarkdownTableExporter(ExportStrategy):
    def export(self, rows: list[dict]) -> str:
        headers = list(rows[0].keys())
        body = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
        for row in rows:
            body.append("| " + " | ".join(str(row[key]) for key in headers) + " |")
        return "\n".join(body)


class ReportExporter:
    def __init__(self, strategy: ExportStrategy):
        self.strategy = strategy

    def export(self, rows: list[dict]) -> str:
        return self.strategy.export(rows)

    def export_many(self, rows: list[dict], strategies: list[ExportStrategy]) -> list[str]:
        return [strategy.export(rows) for strategy in strategies]


# Task 4
class RouteStrategy(ABC):
    @abstractmethod
    def build(self, distance: float) -> str:
        pass


class CarRoute(RouteStrategy):
    def build(self, distance: float) -> str:
        return f"Car: {distance / 60:.1f} ч"


class WalkingRoute(RouteStrategy):
    def build(self, distance: float) -> str:
        return f"Walk: {distance / 5:.1f} ч"


class BicycleRoute(RouteStrategy):
    def build(self, distance: float) -> str:
        return f"Bike: {distance / 15:.1f} ч"


class PublicTransportRoute(RouteStrategy):
    def build(self, distance: float) -> str:
        return f"Public transport: {distance / 30:.1f} ч с пересадками"


class Navigator:
    def __init__(self, strategy: RouteStrategy):
        self.strategy = strategy

    def choose(self, preference: str) -> None:
        mapping = {
            "car": CarRoute(),
            "walk": WalkingRoute(),
            "bike": BicycleRoute(),
            "public": PublicTransportRoute(),
        }
        self.strategy = mapping[preference]

    def route(self, distance: float) -> str:
        return self.strategy.build(distance)


# Task 5
class FieldRule(ABC):
    @abstractmethod
    def validate(self, value) -> str | None:
        pass


class RequiredValidator(FieldRule):
    def validate(self, value) -> str | None:
        if value in ("", None):
            return "Поле обязательно"
        return None


class LengthValidator(FieldRule):
    def __init__(self, min_length: int, max_length: int):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value) -> str | None:
        if not (self.min_length <= len(value) <= self.max_length):
            return f"Длина должна быть от {self.min_length} до {self.max_length}"
        return None


class RegexValidator(FieldRule):
    def __init__(self, predicate, message: str):
        self.predicate = predicate
        self.message = message

    def validate(self, value) -> str | None:
        if not self.predicate(value):
            return self.message
        return None


class RangeValidator(FieldRule):
    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value) -> str | None:
        if not (self.min_value <= value <= self.max_value):
            return f"Значение должно быть от {self.min_value} до {self.max_value}"
        return None


class UniqueValidator(FieldRule):
    def __init__(self, existing: set):
        self.existing = existing

    def validate(self, value) -> str | None:
        if value in self.existing:
            return "Значение должно быть уникальным"
        return None


class FieldValidator:
    def __init__(self, rules: list[FieldRule]):
        self.rules = rules

    def validate(self, value) -> list[str]:
        errors = []
        for rule in self.rules:
            error = rule.validate(value)
            if error is not None:
                errors.append(error)
        return errors


if __name__ == "__main__":
    print("Task 1")
    sorter = Sorter(BubbleSort())
    data = [5, 2, 8, 1, 3]
    print(sorter.sort(data))
    sorter.set_strategy(QuickSort())
    print(sorter.sort(data))
    sorter.set_strategy(MergeSort())
    print(sorter.sort(data))
    print("-" * 40)

    print("Task 2")
    cart = Cart(total=1000, quantity=6, loyalty_points=50)
    strategies = [NoDiscount(), PercentDiscount(10), FixedDiscount(120), BulkDiscount(5, 15), LoyaltyDiscount()]
    print(cart.best_total(strategies))
    print("-" * 40)

    print("Task 3")
    rows = [{"name": "Анна", "age": 20}, {"name": "Иван", "age": 25}]
    exporter = ReportExporter(JsonExporter())
    print(exporter.export(rows))
    print(exporter.export_many(rows, [CsvExporter(), XmlExporter(), MarkdownTableExporter()]))
    print("-" * 40)

    print("Task 4")
    navigator = Navigator(CarRoute())
    print(navigator.route(120))
    navigator.choose("bike")
    print(navigator.route(30))
    print("-" * 40)

    print("Task 5")
    username_validator = FieldValidator([RequiredValidator(), LengthValidator(3, 10), UniqueValidator({"admin"})])
    age_validator = FieldValidator([RangeValidator(18, 99)])
    email_validator = FieldValidator([RegexValidator(lambda value: "@" in value, "Некорректный email")])
    print(username_validator.validate("ad"))
    print(age_validator.validate(17))
    print(email_validator.validate("test"))

from __future__ import annotations

import json
from abc import ABC, abstractmethod


# Task 1
class DocumentParser(ABC):
    def parse(self, raw: str) -> dict:
        self.open_file(raw)
        self.before_parse()
        header = self.parse_header(raw)
        body = self.parse_body(raw)
        metadata = self.extract_metadata(raw)
        self.close_file()
        return {"header": header, "body": body, "metadata": metadata}

    def open_file(self, raw: str) -> None:
        print(f"open: {len(raw)} chars")

    def before_parse(self) -> None:
        pass

    @abstractmethod
    def parse_header(self, raw: str):
        pass

    @abstractmethod
    def parse_body(self, raw: str):
        pass

    @abstractmethod
    def extract_metadata(self, raw: str):
        pass

    def close_file(self) -> None:
        print("close file")


class CsvParser(DocumentParser):
    def before_parse(self) -> None:
        print("prepare csv")

    def parse_header(self, raw: str):
        return raw.splitlines()[0].split(",")

    def parse_body(self, raw: str):
        return [line.split(",") for line in raw.splitlines()[1:]]

    def extract_metadata(self, raw: str):
        return {"rows": max(0, len(raw.splitlines()) - 1)}


class JsonParser(DocumentParser):
    def before_parse(self) -> None:
        print("prepare json")

    def parse_header(self, raw: str):
        data = json.loads(raw)
        return list(data[0].keys())

    def parse_body(self, raw: str):
        return json.loads(raw)

    def extract_metadata(self, raw: str):
        return {"type": "json"}


class HtmlParser(DocumentParser):
    def before_parse(self) -> None:
        print("prepare html")

    def parse_header(self, raw: str):
        return raw.split(">", 1)[0] + ">"

    def parse_body(self, raw: str):
        return raw

    def extract_metadata(self, raw: str):
        return {"has_title": "<title>" in raw}


# Task 2
class ReportGenerator(ABC):
    def generate(self):
        data = self.collect_data()
        data = self.filter_data(data)
        aggregated = self.aggregate(data)
        aggregated = self.after_aggregate(aggregated)
        formatted = self.format(aggregated)
        return self.save(formatted)

    @abstractmethod
    def collect_data(self):
        pass

    def filter_data(self, data):
        return data

    @abstractmethod
    def aggregate(self, data):
        pass

    def after_aggregate(self, aggregated):
        return aggregated

    @abstractmethod
    def format(self, aggregated):
        pass

    def save(self, formatted):
        return f"saved::{formatted}"


class SalesReport(ReportGenerator):
    def collect_data(self):
        return [{"region": "RU", "amount": 100}, {"region": "KZ", "amount": 50}]

    def filter_data(self, data):
        return [item for item in data if item["amount"] > 60]

    def aggregate(self, data):
        return {"total": sum(item["amount"] for item in data)}

    def after_aggregate(self, aggregated):
        aggregated["currency"] = "RUB"
        return aggregated

    def format(self, aggregated):
        return f"sales::{aggregated}"


class UserActivityReport(ReportGenerator):
    def collect_data(self):
        return [{"user": "anna", "actions": 3}, {"user": "ivan", "actions": 7}]

    def filter_data(self, data):
        return [item for item in data if item["actions"] >= 3]

    def aggregate(self, data):
        return {"users": len(data), "actions": sum(item["actions"] for item in data)}

    def after_aggregate(self, aggregated):
        aggregated["average"] = aggregated["actions"] / aggregated["users"]
        return aggregated

    def format(self, aggregated):
        return f"activity::{aggregated}"


# Task 3
class ImageProcessor(ABC):
    def process(self, image: dict) -> dict:
        image = self.load(image)
        self.validate(image)
        image = self.preprocess(image)
        image = self.apply_filter(image)
        image = self.postprocess(image)
        return self.save(image)

    def load(self, image: dict) -> dict:
        image = dict(image)
        image["loaded"] = True
        return image

    def validate(self, image: dict) -> None:
        if "name" not in image:
            raise ValueError("Нет изображения")

    def preprocess(self, image: dict) -> dict:
        return image

    @abstractmethod
    def apply_filter(self, image: dict) -> dict:
        pass

    def postprocess(self, image: dict) -> dict:
        image["processed"] = True
        return image

    def save(self, image: dict) -> dict:
        image["saved"] = True
        return image


class ThumbnailProcessor(ImageProcessor):
    def preprocess(self, image: dict) -> dict:
        image["crop"] = "center"
        return image

    def apply_filter(self, image: dict) -> dict:
        image["size"] = "150x150"
        return image


class WatermarkProcessor(ImageProcessor):
    def apply_filter(self, image: dict) -> dict:
        image["watermark"] = "OpenAI"
        return image


class GrayscaleProcessor(ImageProcessor):
    def apply_filter(self, image: dict) -> dict:
        image["mode"] = "grayscale"
        image["contrast"] = "high"
        return image


# Task 4
class CheckoutProcess(ABC):
    def run(self, cart: dict) -> list[str]:
        steps = [
            self.validate_cart(cart),
            self.apply_discounts(cart),
            self.calculate_shipping(cart),
            self.process_payment(cart),
            self.create_order(cart),
            self.send_notification(cart),
        ]
        return steps

    def validate_cart(self, cart: dict) -> str:
        if not cart["items"]:
            raise ValueError("Корзина пуста")
        return "Корзина валидна"

    def apply_discounts(self, cart: dict) -> str:
        return "Скидки применены"

    def calculate_shipping(self, cart: dict) -> str:
        return "Доставка рассчитана"

    @abstractmethod
    def process_payment(self, cart: dict) -> str:
        pass

    def create_order(self, cart: dict) -> str:
        return "Заказ создан"

    def send_notification(self, cart: dict) -> str:
        return "Уведомление отправлено"


class StandardCheckout(CheckoutProcess):
    def process_payment(self, cart: dict) -> str:
        return "Оплата стандартным способом"


class GuestCheckout(CheckoutProcess):
    def process_payment(self, cart: dict) -> str:
        return "Оплата гостя"

    def create_order(self, cart: dict) -> str:
        return "Заказ создан без аккаунта"


class SubscriptionCheckout(CheckoutProcess):
    def process_payment(self, cart: dict) -> str:
        return "Повторный платеж по подписке"


# Task 5
class BaseTest(ABC):
    def run_test(self) -> dict:
        self.show_instructions()
        self.before_questions()
        questions = self.give_questions()
        answers = self.collect_answers(questions)
        score = self.evaluate(questions, answers)
        return self.show_result(score, len(questions))

    def show_instructions(self) -> None:
        print("Следуйте инструкциям")

    def before_questions(self) -> None:
        pass

    @abstractmethod
    def give_questions(self) -> list[dict]:
        pass

    @abstractmethod
    def collect_answers(self, questions: list[dict]) -> list:
        pass

    @abstractmethod
    def evaluate(self, questions: list[dict], answers: list) -> int:
        pass

    def show_result(self, score: int, total: int) -> dict:
        return {"score": score, "total": total}


class MultipleChoiceTest(BaseTest):
    def give_questions(self) -> list[dict]:
        return [{"question": "2+2", "correct": "4"}]

    def collect_answers(self, questions: list[dict]) -> list:
        return ["4"]

    def evaluate(self, questions: list[dict], answers: list) -> int:
        return sum(question["correct"] == answer for question, answer in zip(questions, answers))


class OpenAnswerTest(BaseTest):
    def give_questions(self) -> list[dict]:
        return [{"question": "Язык программирования", "keywords": {"python", "питон"}}]

    def collect_answers(self, questions: list[dict]) -> list:
        return ["Python"]

    def evaluate(self, questions: list[dict], answers: list) -> int:
        score = 0
        for question, answer in zip(questions, answers):
            if answer.lower() in question["keywords"]:
                score += 1
        return score


class TimedTest(BaseTest):
    def before_questions(self) -> None:
        print("Запущен таймер")

    def give_questions(self) -> list[dict]:
        return [{"question": "Столица Франции", "correct": "Париж"}]

    def collect_answers(self, questions: list[dict]) -> list:
        return ["Париж"]

    def evaluate(self, questions: list[dict], answers: list) -> int:
        return sum(question["correct"] == answer for question, answer in zip(questions, answers))


if __name__ == "__main__":
    print("Task 1")
    print(CsvParser().parse("name,age\nАнна,20"))
    print(JsonParser().parse('[{"name": "Иван"}]'))
    print(HtmlParser().parse("<html><title>Hello</title></html>"))
    print("-" * 40)

    print("Task 2")
    print(SalesReport().generate())
    print(UserActivityReport().generate())
    print("-" * 40)

    print("Task 3")
    print(ThumbnailProcessor().process({"name": "photo.png"}))
    print(WatermarkProcessor().process({"name": "photo.png"}))
    print(GrayscaleProcessor().process({"name": "photo.png"}))
    print("-" * 40)

    print("Task 4")
    cart = {"items": ["book"], "user": "anna"}
    print(StandardCheckout().run(cart))
    print(GuestCheckout().run(cart))
    print(SubscriptionCheckout().run(cart))
    print("-" * 40)

    print("Task 5")
    print(MultipleChoiceTest().run_test())
    print(OpenAnswerTest().run_test())
    print(TimedTest().run_test())

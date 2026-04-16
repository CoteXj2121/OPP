from __future__ import annotations

from abc import ABC, abstractmethod


# Task 1
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float, currency: str) -> str:
        pass


class StripeSDK:
    def create_charge(self, amount_cents: int, currency_code: str) -> str:
        return f"Stripe charge: {amount_cents} {currency_code}"


class StripeAdapter(PaymentProcessor):
    def __init__(self, sdk: StripeSDK):
        self.sdk = sdk

    def pay(self, amount: float, currency: str) -> str:
        return self.sdk.create_charge(int(amount * 100), currency.upper())


# Task 2
class Logger(ABC):
    @abstractmethod
    def info(self, message: str) -> None:
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        pass


class MonologLogger:
    def write(self, level: str, text: str) -> None:
        print(f"[{level.upper()}] {text}")


class MonologAdapter(Logger):
    def __init__(self, monolog: MonologLogger):
        self.monolog = monolog

    def info(self, message: str) -> None:
        self.monolog.write("info", message)

    def warning(self, message: str) -> None:
        self.monolog.write("warning", message)

    def error(self, message: str) -> None:
        self.monolog.write("error", message)


# Task 3
class DataReader(ABC):
    @abstractmethod
    def read_all(self) -> list[dict]:
        pass

    @abstractmethod
    def read_by_id(self, item_id: int) -> dict | None:
        pass


class CsvFileReader:
    def fetch_rows(self) -> list[dict]:
        return [{"id": 1, "name": "Анна"}, {"id": 2, "name": "Иван"}]


class JsonApiClient:
    def get_items(self) -> dict:
        return {"items": [{"id": 10, "name": "Report"}, {"id": 11, "name": "Invoice"}]}


class CsvReaderAdapter(DataReader):
    def __init__(self, reader: CsvFileReader):
        self.reader = reader

    def read_all(self) -> list[dict]:
        return self.reader.fetch_rows()

    def read_by_id(self, item_id: int) -> dict | None:
        return next((row for row in self.read_all() if row["id"] == item_id), None)


class JsonApiAdapter(DataReader):
    def __init__(self, client: JsonApiClient):
        self.client = client

    def read_all(self) -> list[dict]:
        return self.client.get_items()["items"]

    def read_by_id(self, item_id: int) -> dict | None:
        return next((row for row in self.read_all() if row["id"] == item_id), None)


# Task 4
class GeoService(ABC):
    @abstractmethod
    def get_coordinates(self, address: str) -> tuple[float, float]:
        pass

    @abstractmethod
    def get_address(self, latitude: float, longitude: float) -> str:
        pass


class GoogleMapsAPI:
    def geocode(self, address: str) -> dict:
        return {"lat": 55.75, "lng": 37.61, "formatted_address": address}

    def reverse_geocode(self, lat: float, lng: float) -> dict:
        return {"formatted_address": f"Google Address ({lat}, {lng})"}


class YandexMapsAPI:
    def find(self, address: str) -> dict:
        return {"position": {"latitude": 59.93, "longitude": 30.31}, "address": address}

    def resolve(self, lat: float, lng: float) -> dict:
        return {"result": {"address_line": f"Yandex Address ({lat}, {lng})"}}


class GoogleMapsAdapter(GeoService):
    def __init__(self, api: GoogleMapsAPI):
        self.api = api

    def get_coordinates(self, address: str) -> tuple[float, float]:
        result = self.api.geocode(address)
        return result["lat"], result["lng"]

    def get_address(self, latitude: float, longitude: float) -> str:
        return self.api.reverse_geocode(latitude, longitude)["formatted_address"]


class YandexMapsAdapter(GeoService):
    def __init__(self, api: YandexMapsAPI):
        self.api = api

    def get_coordinates(self, address: str) -> tuple[float, float]:
        result = self.api.find(address)
        return result["position"]["latitude"], result["position"]["longitude"]

    def get_address(self, latitude: float, longitude: float) -> str:
        return self.api.resolve(latitude, longitude)["result"]["address_line"]


# Task 5
class CelsiusSensor(ABC):
    @abstractmethod
    def get_celsius(self) -> float:
        pass

    @abstractmethod
    def set_celsius(self, value: float) -> None:
        pass


class FahrenheitSensor(ABC):
    @abstractmethod
    def get_fahrenheit(self) -> float:
        pass

    @abstractmethod
    def set_fahrenheit(self, value: float) -> None:
        pass


class CelsiusStation(CelsiusSensor):
    def __init__(self, value: float):
        self.value = value

    def get_celsius(self) -> float:
        return self.value

    def set_celsius(self, value: float) -> None:
        self.value = value


class FahrenheitStation(FahrenheitSensor):
    def __init__(self, value: float):
        self.value = value

    def get_fahrenheit(self) -> float:
        return self.value

    def set_fahrenheit(self, value: float) -> None:
        self.value = value


class TemperatureAdapter(CelsiusSensor, FahrenheitSensor):
    def __init__(self, sensor: object):
        self.sensor = sensor

    def get_celsius(self) -> float:
        if isinstance(self.sensor, CelsiusSensor):
            return self.sensor.get_celsius()
        return (self.sensor.get_fahrenheit() - 32) * 5 / 9

    def set_celsius(self, value: float) -> None:
        if isinstance(self.sensor, CelsiusSensor):
            self.sensor.set_celsius(value)
        else:
            self.sensor.set_fahrenheit(value * 9 / 5 + 32)

    def get_fahrenheit(self) -> float:
        if isinstance(self.sensor, FahrenheitSensor):
            return self.sensor.get_fahrenheit()
        return self.sensor.get_celsius() * 9 / 5 + 32

    def set_fahrenheit(self, value: float) -> None:
        if isinstance(self.sensor, FahrenheitSensor):
            self.sensor.set_fahrenheit(value)
        else:
            self.sensor.set_celsius((value - 32) * 5 / 9)


if __name__ == "__main__":
    print("Task 1")
    processor: PaymentProcessor = StripeAdapter(StripeSDK())
    print(processor.pay(19.99, "usd"))
    print("-" * 40)

    print("Task 2")
    logger: Logger = MonologAdapter(MonologLogger())
    logger.info("Приложение запущено")
    logger.warning("Мало памяти")
    logger.error("Ошибка подключения")
    print("-" * 40)

    print("Task 3")
    readers: list[DataReader] = [CsvReaderAdapter(CsvFileReader()), JsonApiAdapter(JsonApiClient())]
    for reader in readers:
        print(reader.read_all())
        print(reader.read_by_id(1) or reader.read_by_id(10))
    print("-" * 40)

    print("Task 4")
    google = GoogleMapsAdapter(GoogleMapsAPI())
    yandex = YandexMapsAdapter(YandexMapsAPI())
    print(google.get_coordinates("Москва"))
    print(yandex.get_address(59.93, 30.31))
    print("-" * 40)

    print("Task 5")
    celsius_adapter = TemperatureAdapter(CelsiusStation(20))
    fahrenheit_adapter = TemperatureAdapter(FahrenheitStation(68))
    print(celsius_adapter.get_fahrenheit())
    print(fahrenheit_adapter.get_celsius())

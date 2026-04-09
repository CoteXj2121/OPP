from __future__ import annotations

from abc import ABC, abstractmethod
import csv
import io
import json
import xml.etree.ElementTree as ET


class Parser(ABC):
    @abstractmethod
    def parse(self, raw: str) -> list[dict]:
        pass


class JsonParser(Parser):
    def parse(self, raw: str) -> list[dict]:
        return json.loads(raw)


class CsvParser(Parser):
    def parse(self, raw: str) -> list[dict]:
        return list(csv.DictReader(io.StringIO(raw)))


class XmlParser(Parser):
    def parse(self, raw: str) -> list[dict]:
        root = ET.fromstring(raw)
        return [{child.tag: child.text for child in item} for item in root]


class DataImporter(ABC):
    @abstractmethod
    def create_parser(self) -> Parser:
        pass

    def parse(self, raw: str) -> list[dict]:
        parser = self.create_parser()
        return parser.parse(raw)


class JsonImporter(DataImporter):
    def create_parser(self) -> Parser:
        return JsonParser()


class CsvImporter(DataImporter):
    def create_parser(self) -> Parser:
        return CsvParser()


class XmlImporter(DataImporter):
    def create_parser(self) -> Parser:
        return XmlParser()


if __name__ == "__main__":
    json_data = '[{"name": "Анна", "age": 20}, {"name": "Игорь", "age": 22}]'
    csv_data = "name,age\nАнна,20\nИгорь,22"
    xml_data = (
        "<items>"
        "<item><name>Анна</name><age>20</age></item>"
        "<item><name>Игорь</name><age>22</age></item>"
        "</items>"
    )

    print(JsonImporter().parse(json_data))
    print(CsvImporter().parse(csv_data))
    print(XmlImporter().parse(xml_data))

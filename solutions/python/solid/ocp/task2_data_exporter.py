from abc import ABC, abstractmethod
import csv
import io
import json
import xml.etree.ElementTree as et


class ExportFormat(ABC):
    @abstractmethod
    def export(self, data: list[dict]) -> str:
        pass


class JsonExport(ExportFormat):
    def export(self, data: list[dict]) -> str:
        return json.dumps(data, ensure_ascii=False)


class CsvExport(ExportFormat):
    def export(self, data: list[dict]) -> str:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()


class XmlExport(ExportFormat):
    def export(self, data: list[dict]) -> str:
        root = et.Element("records")
        for item in data:
            record = et.SubElement(root, "record")
            for key, value in item.items():
                node = et.SubElement(record, key)
                node.text = str(value)
        return et.tostring(root, encoding="unicode")


class DataExporter:
    def export(self, data: list[dict], export_format: ExportFormat) -> str:
        return export_format.export(data)


if __name__ == "__main__":
    records = [{"name": "Анна", "age": 30}, {"name": "Иван", "age": 25}]
    exporter = DataExporter()

    print(exporter.export(records, JsonExport()))
    print(exporter.export(records, CsvExport()))
    print(exporter.export(records, XmlExport()))

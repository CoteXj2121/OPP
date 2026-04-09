from __future__ import annotations

from abc import ABC, abstractmethod


class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        pass


class PdfReport(ReportGenerator):
    def generate(self, data: dict) -> str:
        return f"[PDF] Отчёт: {data}"


class ExcelReport(ReportGenerator):
    def generate(self, data: dict) -> str:
        return f"[Excel] Отчёт: {data}"


class CsvReport(ReportGenerator):
    def generate(self, data: dict) -> str:
        return f"[CSV] Отчёт: {data}"


class ReportManager(ABC):
    @abstractmethod
    def create_generator(self) -> ReportGenerator:
        pass

    def export(self, data: dict) -> str:
        generator = self.create_generator()
        return generator.generate(data)


class PdfReportManager(ReportManager):
    def create_generator(self) -> ReportGenerator:
        return PdfReport()


class ExcelReportManager(ReportManager):
    def create_generator(self) -> ReportGenerator:
        return ExcelReport()


class CsvReportManager(ReportManager):
    def create_generator(self) -> ReportGenerator:
        return CsvReport()


if __name__ == "__main__":
    report_data = {"title": "Продажи Q1", "total": 150000}

    print(PdfReportManager().export(report_data))
    print(ExcelReportManager().export(report_data))
    print(CsvReportManager().export(report_data))

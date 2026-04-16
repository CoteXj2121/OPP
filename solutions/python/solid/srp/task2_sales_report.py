class SalesReport:
    def __init__(self, data: list[dict]):
        self.data = data

    def get_total(self) -> float:
        return sum(item["amount"] for item in self.data)


class HtmlReportFormatter:
    def format(self, report: SalesReport) -> str:
        rows = "".join(
            f"<tr><td>{item['name']}</td><td>{item['amount']}</td></tr>"
            for item in report.data
        )
        return (
            f"<table>{rows}<tr><td>Итого</td><td>{report.get_total()}</td></tr></table>"
        )


if __name__ == "__main__":
    report = SalesReport(
        [
            {"name": "Товар A", "amount": 1500},
            {"name": "Товар B", "amount": 2300},
        ]
    )
    formatter = HtmlReportFormatter()

    print(formatter.format(report))

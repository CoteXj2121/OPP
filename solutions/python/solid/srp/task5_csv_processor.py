import csv
import io
import tempfile
from pathlib import Path


class CsvParser:
    def parse(self, csv_content: str) -> list[dict[str, str]]:
        reader = csv.DictReader(io.StringIO(csv_content))
        return [row for row in reader]


class CsvWriter:
    def write(self, rows: list[dict[str, str]], output_path: Path) -> None:
        if not rows:
            output_path.write_text("", encoding="utf-8")
            return

        with output_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    content = "name,age\nАнна,30\nИван,25"
    parser = CsvParser()
    writer = CsvWriter()

    rows = parser.parse(content)
    output_path = Path(tempfile.gettempdir()) / "srp_task5_output.csv"
    writer.write(rows, output_path)

    for row in rows:
        print(row)
    print(f"Файл сохранен: {output_path}")

from abc import ABC, abstractmethod


class Printable(ABC):
    @abstractmethod
    def print_doc(self, document: str) -> None:
        pass


class Scannable(ABC):
    @abstractmethod
    def scan_doc(self, document: str) -> None:
        pass


class Faxable(ABC):
    @abstractmethod
    def send_fax(self, document: str) -> None:
        pass


class AdvancedPrinter(Printable, Scannable, Faxable):
    def print_doc(self, document: str) -> None:
        print(f"Печать: {document}")

    def scan_doc(self, document: str) -> None:
        print(f"Сканирование: {document}")

    def send_fax(self, document: str) -> None:
        print(f"Отправка факса: {document}")


class SimplePrinter(Printable):
    def print_doc(self, document: str) -> None:
        print(f"Печать: {document}")


if __name__ == "__main__":
    simple_printer = SimplePrinter()
    simple_printer.print_doc("Договор.pdf")

    advanced_printer = AdvancedPrinter()
    advanced_printer.scan_doc("Договор.pdf")
    advanced_printer.send_fax("Договор.pdf")

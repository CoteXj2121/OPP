from __future__ import annotations

from abc import ABC, abstractmethod


# Task 1
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class TextInput(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

    @abstractmethod
    def create_input(self) -> TextInput:
        pass


class LightButton(Button):
    def render(self) -> str:
        return "Светлая кнопка"


class DarkButton(Button):
    def render(self) -> str:
        return "Темная кнопка"


class LightCheckbox(Checkbox):
    def render(self) -> str:
        return "Светлый чекбокс"


class DarkCheckbox(Checkbox):
    def render(self) -> str:
        return "Темный чекбокс"


class LightInput(TextInput):
    def render(self) -> str:
        return "Светлое поле ввода"


class DarkInput(TextInput):
    def render(self) -> str:
        return "Темное поле ввода"


class LightThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return LightButton()

    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()

    def create_input(self) -> TextInput:
        return LightInput()


class DarkThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return DarkButton()

    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()

    def create_input(self) -> TextInput:
        return DarkInput()


def build_ui(factory: UIFactory) -> list[str]:
    return [
        factory.create_button().render(),
        factory.create_checkbox().render(),
        factory.create_input().render(),
    ]


# Task 2
class Connection(ABC):
    @abstractmethod
    def connect(self) -> str:
        pass


class QueryBuilder(ABC):
    @abstractmethod
    def select_all(self, table: str) -> str:
        pass


class Transaction(ABC):
    @abstractmethod
    def begin(self) -> str:
        pass


class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self) -> Connection:
        pass

    @abstractmethod
    def create_query_builder(self) -> QueryBuilder:
        pass

    @abstractmethod
    def create_transaction(self) -> Transaction:
        pass


class MySQLConnection(Connection):
    def connect(self) -> str:
        return "Подключение к MySQL"


class PostgreSQLConnection(Connection):
    def connect(self) -> str:
        return "Подключение к PostgreSQL"


class MySQLQueryBuilder(QueryBuilder):
    def select_all(self, table: str) -> str:
        return f"SELECT * FROM `{table}`;"


class PostgreSQLQueryBuilder(QueryBuilder):
    def select_all(self, table: str) -> str:
        return f'SELECT * FROM "{table}";'


class MySQLTransaction(Transaction):
    def begin(self) -> str:
        return "START TRANSACTION (MySQL)"


class PostgreSQLTransaction(Transaction):
    def begin(self) -> str:
        return "BEGIN (PostgreSQL)"


class MySQLFactory(DatabaseFactory):
    def create_connection(self) -> Connection:
        return MySQLConnection()

    def create_query_builder(self) -> QueryBuilder:
        return MySQLQueryBuilder()

    def create_transaction(self) -> Transaction:
        return MySQLTransaction()


class PostgreSQLFactory(DatabaseFactory):
    def create_connection(self) -> Connection:
        return PostgreSQLConnection()

    def create_query_builder(self) -> QueryBuilder:
        return PostgreSQLQueryBuilder()

    def create_transaction(self) -> Transaction:
        return PostgreSQLTransaction()


def run_database(factory: DatabaseFactory) -> list[str]:
    connection = factory.create_connection()
    builder = factory.create_query_builder()
    transaction = factory.create_transaction()
    return [
        connection.connect(),
        transaction.begin(),
        builder.select_all("users"),
    ]


# Task 3
class Toast(ABC):
    @abstractmethod
    def show(self, message: str) -> str:
        pass


class Dialog(ABC):
    @abstractmethod
    def open(self, title: str) -> str:
        pass


class ProgressBar(ABC):
    @abstractmethod
    def update(self, value: int) -> str:
        pass


class MobileUiFactory(ABC):
    @abstractmethod
    def create_toast(self) -> Toast:
        pass

    @abstractmethod
    def create_dialog(self) -> Dialog:
        pass

    @abstractmethod
    def create_progress_bar(self) -> ProgressBar:
        pass


class IosToast(Toast):
    def show(self, message: str) -> str:
        return f"iOS toast: {message}"


class AndroidToast(Toast):
    def show(self, message: str) -> str:
        return f"Android toast: {message}"


class IosDialog(Dialog):
    def open(self, title: str) -> str:
        return f"iOS dialog: {title}"


class AndroidDialog(Dialog):
    def open(self, title: str) -> str:
        return f"Android dialog: {title}"


class IosProgressBar(ProgressBar):
    def update(self, value: int) -> str:
        return f"iOS progress: {value}%"


class AndroidProgressBar(ProgressBar):
    def update(self, value: int) -> str:
        return f"Android progress: {value}%"


class IosFactory(MobileUiFactory):
    def create_toast(self) -> Toast:
        return IosToast()

    def create_dialog(self) -> Dialog:
        return IosDialog()

    def create_progress_bar(self) -> ProgressBar:
        return IosProgressBar()


class AndroidFactory(MobileUiFactory):
    def create_toast(self) -> Toast:
        return AndroidToast()

    def create_dialog(self) -> Dialog:
        return AndroidDialog()

    def create_progress_bar(self) -> ProgressBar:
        return AndroidProgressBar()


def show_mobile_message(factory: MobileUiFactory) -> list[str]:
    return [
        factory.create_toast().show("Файл загружен"),
        factory.create_dialog().open("Подтверждение"),
        factory.create_progress_bar().update(75),
    ]


# Task 4
class Header(ABC):
    @abstractmethod
    def render(self, title: str) -> str:
        pass


class Table(ABC):
    @abstractmethod
    def render(self, rows: list[list[str]]) -> str:
        pass


class Footer(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class DocumentFactory(ABC):
    @abstractmethod
    def create_header(self) -> Header:
        pass

    @abstractmethod
    def create_table(self) -> Table:
        pass

    @abstractmethod
    def create_footer(self) -> Footer:
        pass


class PdfHeader(Header):
    def render(self, title: str) -> str:
        return f"[PDF Header] {title}"


class DocxHeader(Header):
    def render(self, title: str) -> str:
        return f"[DOCX Header] {title}"


class PdfTable(Table):
    def render(self, rows: list[list[str]]) -> str:
        return f"[PDF Table] {rows}"


class DocxTable(Table):
    def render(self, rows: list[list[str]]) -> str:
        return f"[DOCX Table] {rows}"


class PdfFooter(Footer):
    def render(self) -> str:
        return "[PDF Footer]"


class DocxFooter(Footer):
    def render(self) -> str:
        return "[DOCX Footer]"


class PdfDocumentFactory(DocumentFactory):
    def create_header(self) -> Header:
        return PdfHeader()

    def create_table(self) -> Table:
        return PdfTable()

    def create_footer(self) -> Footer:
        return PdfFooter()


class DocxDocumentFactory(DocumentFactory):
    def create_header(self) -> Header:
        return DocxHeader()

    def create_table(self) -> Table:
        return DocxTable()

    def create_footer(self) -> Footer:
        return DocxFooter()


def build_document(factory: DocumentFactory, title: str, rows: list[list[str]]) -> list[str]:
    return [
        factory.create_header().render(title),
        factory.create_table().render(rows),
        factory.create_footer().render(),
    ]


# Task 5
class Hero(ABC):
    @abstractmethod
    def action(self) -> str:
        pass


class Enemy(ABC):
    @abstractmethod
    def action(self) -> str:
        pass


class Weapon(ABC):
    @abstractmethod
    def action(self) -> str:
        pass


class WorldFactory(ABC):
    @abstractmethod
    def create_hero(self) -> Hero:
        pass

    @abstractmethod
    def create_enemy(self) -> Enemy:
        pass

    @abstractmethod
    def create_weapon(self) -> Weapon:
        pass


class FantasyHero(Hero):
    def action(self) -> str:
        return "Рыцарь идет в бой"


class FantasyEnemy(Enemy):
    def action(self) -> str:
        return "Дракон атакует"


class FantasyWeapon(Weapon):
    def action(self) -> str:
        return "Меч готов к удару"


class SciFiHero(Hero):
    def action(self) -> str:
        return "Космодесантник занимает позицию"


class SciFiEnemy(Enemy):
    def action(self) -> str:
        return "Боевой дрон открывает огонь"


class SciFiWeapon(Weapon):
    def action(self) -> str:
        return "Лазерная винтовка заряжена"


class FantasyWorldFactory(WorldFactory):
    def create_hero(self) -> Hero:
        return FantasyHero()

    def create_enemy(self) -> Enemy:
        return FantasyEnemy()

    def create_weapon(self) -> Weapon:
        return FantasyWeapon()


class SciFiWorldFactory(WorldFactory):
    def create_hero(self) -> Hero:
        return SciFiHero()

    def create_enemy(self) -> Enemy:
        return SciFiEnemy()

    def create_weapon(self) -> Weapon:
        return SciFiWeapon()


def create_world(factory: WorldFactory) -> list[str]:
    hero = factory.create_hero()
    enemy = factory.create_enemy()
    weapon = factory.create_weapon()
    return [hero.action(), enemy.action(), weapon.action()]


if __name__ == "__main__":
    print("Task 1")
    print(build_ui(LightThemeFactory()))
    print(build_ui(DarkThemeFactory()))
    print("-" * 40)

    print("Task 2")
    print(run_database(MySQLFactory()))
    print(run_database(PostgreSQLFactory()))
    print("-" * 40)

    print("Task 3")
    print(show_mobile_message(IosFactory()))
    print(show_mobile_message(AndroidFactory()))
    print("-" * 40)

    print("Task 4")
    rows = [["Товар", "Цена"], ["Книга", "350"]]
    print(build_document(PdfDocumentFactory(), "Отчет", rows))
    print(build_document(DocxDocumentFactory(), "Отчет", rows))
    print("-" * 40)

    print("Task 5")
    print(create_world(FantasyWorldFactory()))
    print(create_world(SciFiWorldFactory()))

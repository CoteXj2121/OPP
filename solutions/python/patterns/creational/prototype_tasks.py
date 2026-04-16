from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime


# Task 1
@dataclass
class Stats:
    hp: int
    mana: int
    strength: int


@dataclass
class Ability:
    name: str
    power: int


@dataclass
class Character:
    name: str
    stats: Stats
    abilities: list[Ability]

    def clone(self) -> Character:
        return deepcopy(self)


# Task 2
class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        pass


@dataclass
class Button(Cloneable):
    text: str
    color: str

    def clone(self) -> Button:
        return deepcopy(self)


@dataclass
class Card(Cloneable):
    title: str
    body: str

    def clone(self) -> Card:
        return deepcopy(self)


@dataclass
class Modal(Cloneable):
    title: str
    size: str

    def clone(self) -> Modal:
        return deepcopy(self)


class ComponentRegistry:
    def __init__(self):
        self._items: dict[str, Cloneable] = {}

    def register(self, name: str, component: Cloneable) -> None:
        self._items[name] = component

    def create(self, name: str):
        return self._items[name].clone()


# Task 3
@dataclass
class DatabaseConfig:
    host: str
    port: int
    db_name: str


@dataclass
class ServerConfig:
    env_name: str
    debug: bool
    database: DatabaseConfig

    def clone(self) -> ServerConfig:
        return deepcopy(self)


# Task 4
@dataclass
class Metadata:
    author: str
    created_at: datetime
    version: int


@dataclass
class Document:
    text: str
    tags: list[str]
    metadata: Metadata
    history: list[str] = field(default_factory=list)

    def clone(self) -> Document:
        new_document = deepcopy(self)
        new_document.metadata.version += 1
        new_document.metadata.created_at = datetime.now()
        new_document.history = []
        return new_document


# Task 5
@dataclass
class SenderInfo:
    name: str
    email: str


@dataclass
class EmailTemplate:
    subject: str
    html_body: str
    recipients: list[str]
    sender: SenderInfo

    def clone(self) -> EmailTemplate:
        return deepcopy(self)


class TemplateRegistry:
    def __init__(self):
        self._templates: dict[str, EmailTemplate] = {}

    def register(self, name: str, template: EmailTemplate) -> None:
        self._templates[name] = template

    def get(self, name: str) -> EmailTemplate:
        return self._templates[name].clone()


class MailingManager:
    def __init__(self, registry: TemplateRegistry):
        self.registry = registry

    def send_personalized(self, template_name: str, recipient: str, username: str) -> EmailTemplate:
        template = self.registry.get(template_name)
        template.recipients = [recipient]
        template.subject = template.subject.replace("{name}", username)
        template.html_body = template.html_body.replace("{name}", username)
        print(f"Отправка письма {recipient} от {template.sender.email}")
        return template


if __name__ == "__main__":
    print("Task 1")
    original = Character("Mage", Stats(100, 200, 15), [Ability("Fireball", 50)])
    clone = original.clone()
    clone.stats.hp = 50
    clone.abilities.append(Ability("Ice", 30))
    print(original)
    print(clone)
    print("-" * 40)

    print("Task 2")
    registry = ComponentRegistry()
    registry.register("primary_button", Button("Купить", "blue"))
    button = registry.create("primary_button")
    button.text = "Оплатить"
    print(registry.create("primary_button"))
    print(button)
    print("-" * 40)

    print("Task 3")
    base_config = ServerConfig("base", True, DatabaseConfig("localhost", 5432, "app"))
    production = base_config.clone()
    production.env_name = "production"
    production.debug = False
    production.database.host = "prod-db"
    print(base_config)
    print(production)
    print("-" * 40)

    print("Task 4")
    document = Document(
        text="Черновик",
        tags=["draft"],
        metadata=Metadata("Алексей", datetime(2026, 4, 16), 1),
        history=["создан документ"],
    )
    document_copy = document.clone()
    print(document)
    print(document_copy)
    print("-" * 40)

    print("Task 5")
    template_registry = TemplateRegistry()
    template_registry.register(
        "welcome",
        EmailTemplate(
            subject="Привет, {name}!",
            html_body="<h1>Добро пожаловать, {name}</h1>",
            recipients=[],
            sender=SenderInfo("Support", "support@example.com"),
        ),
    )
    manager = MailingManager(template_registry)
    print(manager.send_personalized("welcome", "user@example.com", "Иван"))
    print(template_registry.get("welcome"))

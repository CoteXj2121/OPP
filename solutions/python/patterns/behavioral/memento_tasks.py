from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime


# Task 1
@dataclass
class EditorState:
    text: str
    cursor: int


class TextEditor:
    def __init__(self):
        self.text = ""
        self.cursor = 0
        self.undo_stack: list[EditorState] = []
        self.redo_stack: list[EditorState] = []

    def _save(self) -> None:
        self.undo_stack.append(EditorState(self.text, self.cursor))
        self.redo_stack.clear()

    def insert(self, value: str) -> None:
        self._save()
        self.text = self.text[: self.cursor] + value + self.text[self.cursor :]
        self.cursor += len(value)

    def delete(self, count: int) -> None:
        self._save()
        self.text = self.text[: self.cursor] + self.text[self.cursor + count :]

    def move_cursor(self, position: int) -> None:
        self._save()
        self.cursor = max(0, min(position, len(self.text)))

    def undo(self) -> None:
        if not self.undo_stack:
            return
        self.redo_stack.append(EditorState(self.text, self.cursor))
        state = self.undo_stack.pop()
        self.text, self.cursor = state.text, state.cursor

    def redo(self) -> None:
        if not self.redo_stack:
            return
        self.undo_stack.append(EditorState(self.text, self.cursor))
        state = self.redo_stack.pop()
        self.text, self.cursor = state.text, state.cursor


# Task 2
@dataclass
class CharacterState:
    level: int
    hp: int
    position: tuple[int, int]
    inventory: list[str]


@dataclass
class SaveSlot:
    name: str
    saved_at: str
    state: CharacterState


class SaveCaretaker:
    def __init__(self):
        self.slots: dict[str, SaveSlot] = {}

    def save(self, slot_name: str, state: CharacterState) -> None:
        self.slots[slot_name] = SaveSlot(
            slot_name,
            datetime.now().isoformat(timespec="seconds"),
            deepcopy(state),
        )

    def load(self, slot_name: str) -> CharacterState:
        return deepcopy(self.slots[slot_name].state)

    def list_slots(self) -> list[dict]:
        return [
            {"name": slot.name, "saved_at": slot.saved_at, "level": slot.state.level}
            for slot in self.slots.values()
        ]


# Task 3
class ConfigManager:
    def __init__(self):
        self.data: dict[str, str] = {}
        self.transactions: list[dict[str, str]] = []

    def begin(self) -> None:
        self.transactions.append(deepcopy(self.data))

    def set(self, key: str, value: str) -> None:
        self.data[key] = value

    def commit(self) -> None:
        if self.transactions:
            self.transactions.pop()

    def rollback(self) -> None:
        if self.transactions:
            self.data = self.transactions.pop()


# Task 4
@dataclass
class Commit:
    content: str
    message: str
    author: str
    created_at: str


class VersionedDocument:
    def __init__(self, content: str = ""):
        self.content = content
        self.commits: list[Commit] = []

    def commit(self, message: str, author: str) -> None:
        self.commits.append(
            Commit(self.content, message, author, datetime.now().isoformat(timespec="seconds"))
        )

    def checkout(self, index: int) -> None:
        self.content = self.commits[index].content

    def diff(self, left: int, right: int) -> dict[str, list[str]]:
        left_lines = set(self.commits[left].content.splitlines())
        right_lines = set(self.commits[right].content.splitlines())
        return {
            "added": sorted(right_lines - left_lines),
            "removed": sorted(left_lines - right_lines),
        }

    def log(self) -> list[str]:
        return [f"{commit.author}: {commit.message}" for commit in self.commits]


# Task 5
@dataclass
class Shape:
    name: str
    x: int
    y: int
    size: int


@dataclass
class CanvasState:
    shapes: list[Shape]


class Canvas:
    def __init__(self):
        self.shapes: list[Shape] = []
        self.history: list[CanvasState] = []

    def _save(self) -> None:
        self.history.append(CanvasState(deepcopy(self.shapes)))

    def draw(self, shape: Shape) -> None:
        self._save()
        self.shapes.append(shape)

    def move(self, name: str, x: int, y: int) -> None:
        self._save()
        for shape in self.shapes:
            if shape.name == name:
                shape.x = x
                shape.y = y

    def resize(self, name: str, size: int) -> None:
        self._save()
        for shape in self.shapes:
            if shape.name == name:
                shape.size = size

    def delete(self, name: str) -> None:
        self._save()
        self.shapes = [shape for shape in self.shapes if shape.name != name]

    def undo(self) -> None:
        if self.history:
            self.shapes = self.history.pop().shapes


if __name__ == "__main__":
    print("Task 1")
    editor = TextEditor()
    editor.insert("Hello")
    editor.insert(" world")
    editor.move_cursor(5)
    editor.insert(",")
    print(editor.text, editor.cursor)
    editor.undo()
    print(editor.text, editor.cursor)
    editor.redo()
    print(editor.text, editor.cursor)
    print("-" * 40)

    print("Task 2")
    saves = SaveCaretaker()
    hero = CharacterState(5, 80, (10, 20), ["меч", "щит"])
    saves.save("slot1", hero)
    hero.hp = 10
    print(saves.load("slot1"))
    print(saves.list_slots())
    print("-" * 40)

    print("Task 3")
    config = ConfigManager()
    config.set("env", "dev")
    config.begin()
    config.set("debug", "true")
    config.begin()
    config.set("db", "sqlite")
    print(config.data)
    config.rollback()
    print(config.data)
    config.commit()
    print("-" * 40)

    print("Task 4")
    document = VersionedDocument("line1")
    document.commit("init", "Анна")
    document.content = "line1\nline2"
    document.commit("add line2", "Анна")
    print(document.log())
    print(document.diff(0, 1))
    document.checkout(0)
    print(document.content)
    print("-" * 40)

    print("Task 5")
    canvas = Canvas()
    canvas.draw(Shape("circle", 0, 0, 10))
    canvas.move("circle", 5, 5)
    canvas.resize("circle", 15)
    print(canvas.shapes)
    canvas.undo()
    print(canvas.shapes)

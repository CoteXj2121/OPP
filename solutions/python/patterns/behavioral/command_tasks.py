from __future__ import annotations

import heapq
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


# Task 1
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class Editor:
    def __init__(self):
        self.text = ""


class InsertTextCommand(Command):
    def __init__(self, editor: Editor, text: str):
        self.editor = editor
        self.text = text

    def execute(self) -> None:
        self.editor.text += self.text

    def undo(self) -> None:
        self.editor.text = self.editor.text[: -len(self.text)]


class DeleteTextCommand(Command):
    def __init__(self, editor: Editor, length: int):
        self.editor = editor
        self.length = length
        self.deleted = ""

    def execute(self) -> None:
        self.deleted = self.editor.text[-self.length :]
        self.editor.text = self.editor.text[: -self.length]

    def undo(self) -> None:
        self.editor.text += self.deleted


class ReplaceTextCommand(Command):
    def __init__(self, editor: Editor, old: str, new: str):
        self.editor = editor
        self.old = old
        self.new = new

    def execute(self) -> None:
        self.editor.text = self.editor.text.replace(self.old, self.new, 1)

    def undo(self) -> None:
        self.editor.text = self.editor.text.replace(self.new, self.old, 1)


class CommandHistory:
    def __init__(self):
        self.done: list[Command] = []
        self.undone: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self.done.append(command)
        self.undone.clear()

    def undo(self) -> None:
        if not self.done:
            return
        command = self.done.pop()
        command.undo()
        self.undone.append(command)

    def redo(self) -> None:
        if not self.undone:
            return
        command = self.undone.pop()
        command.execute()
        self.done.append(command)


# Task 2
class QueueCommand(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass


class SendEmailCommand(QueueCommand):
    def __init__(self, email: str):
        self.email = email

    def execute(self) -> str:
        return f"Email sent to {self.email}"


class ResizeImageCommand(QueueCommand):
    def __init__(self, filename: str):
        self.filename = filename

    def execute(self) -> str:
        return f"Image {self.filename} resized"


class GenerateReportCommand(QueueCommand):
    def __init__(self, title: str):
        self.title = title

    def execute(self) -> str:
        return f"Report {self.title} generated"


@dataclass(order=True)
class PrioritizedTask:
    priority: int
    task_id: int
    command: QueueCommand = field(compare=False)
    cancelled: bool = field(default=False, compare=False)


class TaskQueue:
    def __init__(self):
        self._queue: list[PrioritizedTask] = []
        self._task_id = 0

    def add(self, command: QueueCommand, priority: int) -> int:
        self._task_id += 1
        task = PrioritizedTask(priority, self._task_id, command)
        heapq.heappush(self._queue, task)
        return task.task_id

    def cancel(self, task_id: int) -> None:
        for task in self._queue:
            if task.task_id == task_id:
                task.cancelled = True

    def run_all(self) -> list[str]:
        results = []
        while self._queue:
            task = heapq.heappop(self._queue)
            if task.cancelled:
                continue
            results.append(task.command.execute())
        return results


# Task 3
class FakeDatabase:
    def __init__(self):
        self.rows: dict[int, dict] = {}


class DbCommand(Command):
    pass


class InsertCommand(DbCommand):
    def __init__(self, database: FakeDatabase, record: dict):
        self.database = database
        self.record = record

    def execute(self) -> None:
        self.database.rows[self.record["id"]] = dict(self.record)

    def undo(self) -> None:
        self.database.rows.pop(self.record["id"], None)


class UpdateCommand(DbCommand):
    def __init__(self, database: FakeDatabase, record_id: int, new_values: dict):
        self.database = database
        self.record_id = record_id
        self.new_values = new_values
        self.old_values: dict | None = None

    def execute(self) -> None:
        self.old_values = dict(self.database.rows[self.record_id])
        self.database.rows[self.record_id].update(self.new_values)

    def undo(self) -> None:
        if self.old_values is not None:
            self.database.rows[self.record_id] = self.old_values


class DeleteCommand(DbCommand):
    def __init__(self, database: FakeDatabase, record_id: int):
        self.database = database
        self.record_id = record_id
        self.deleted: dict | None = None

    def execute(self) -> None:
        self.deleted = self.database.rows.pop(self.record_id, None)

    def undo(self) -> None:
        if self.deleted is not None:
            self.database.rows[self.record_id] = self.deleted


class Transaction:
    def __init__(self):
        self.commands: list[DbCommand] = []
        self.executed: list[DbCommand] = []

    def add(self, command: DbCommand) -> None:
        self.commands.append(command)

    def commit(self) -> None:
        for command in self.commands:
            command.execute()
            self.executed.append(command)

    def rollback(self) -> None:
        while self.executed:
            self.executed.pop().undo()


# Task 4
class Light:
    def on(self) -> str:
        return "Light on"

    def off(self) -> str:
        return "Light off"


class Fan:
    def on(self) -> str:
        return "Fan on"

    def off(self) -> str:
        return "Fan off"


class SecuritySystem:
    def on(self) -> str:
        return "Security armed"

    def off(self) -> str:
        return "Security disarmed"


class HomeCommand(Command):
    def __init__(self, receiver, method_name: str):
        self.receiver = receiver
        self.method_name = method_name
        self.undo_method = "off" if method_name == "on" else "on"

    def execute(self) -> None:
        print(getattr(self.receiver, self.method_name)())

    def undo(self) -> None:
        print(getattr(self.receiver, self.undo_method)())


class MacroCommand(Command):
    def __init__(self, commands: list[Command]):
        self.commands = commands

    def execute(self) -> None:
        for command in self.commands:
            command.execute()

    def undo(self) -> None:
        for command in reversed(self.commands):
            command.undo()


class NoCommand(Command):
    def execute(self) -> None:
        pass

    def undo(self) -> None:
        pass


class SmartRemote:
    def __init__(self):
        self.on_commands: list[Command] = [NoCommand() for _ in range(5)]
        self.off_commands: list[Command] = [NoCommand() for _ in range(5)]
        self.last_command: Command = NoCommand()

    def set_command(self, slot: int, on_command: Command, off_command: Command) -> None:
        self.on_commands[slot] = on_command
        self.off_commands[slot] = off_command

    def press_on(self, slot: int) -> None:
        self.on_commands[slot].execute()
        self.last_command = self.on_commands[slot]

    def press_off(self, slot: int) -> None:
        self.off_commands[slot].execute()
        self.last_command = self.off_commands[slot]

    def undo(self) -> None:
        self.last_command.undo()

    def macro(self, command: Command) -> None:
        command.execute()
        self.last_command = command


# Task 5
class SchedulerCommand(ABC):
    def __init__(self, name: str, fail_once: bool = False):
        self.name = name
        self.fail_once = fail_once
        self.failed_before = False

    def execute(self) -> str:
        if self.fail_once and not self.failed_before:
            self.failed_before = True
            raise RuntimeError(f"{self.name} failed")
        return f"{self.name} done"


class BackupCommand(SchedulerCommand):
    pass


class CleanupCommand(SchedulerCommand):
    pass


class SyncCommand(SchedulerCommand):
    pass


@dataclass
class ExecutionLogEntry:
    task_name: str
    status: str
    timestamp: str


class ExecutionLog:
    def __init__(self):
        self.entries: list[ExecutionLogEntry] = []

    def add(self, task_name: str, status: str) -> None:
        self.entries.append(
            ExecutionLogEntry(task_name, status, datetime.now().isoformat(timespec="seconds"))
        )


class Scheduler:
    def __init__(self, retries: int):
        self.retries = retries
        self.log = ExecutionLog()

    def run(self, commands: list[SchedulerCommand]) -> None:
        for command in commands:
            attempts = 0
            while attempts <= self.retries:
                try:
                    result = command.execute()
                    self.log.add(command.name, result)
                    break
                except RuntimeError as error:
                    attempts += 1
                    if attempts > self.retries:
                        self.log.add(command.name, str(error))


if __name__ == "__main__":
    print("Task 1")
    editor = Editor()
    history = CommandHistory()
    history.execute(InsertTextCommand(editor, "Hello"))
    history.execute(InsertTextCommand(editor, " world"))
    history.execute(ReplaceTextCommand(editor, "world", "Python"))
    print(editor.text)
    history.undo()
    print(editor.text)
    history.redo()
    print(editor.text)
    print("-" * 40)

    print("Task 2")
    queue = TaskQueue()
    queue.add(SendEmailCommand("user@example.com"), priority=2)
    cancelled = queue.add(ResizeImageCommand("photo.png"), priority=1)
    queue.add(GenerateReportCommand("Sales"), priority=3)
    queue.cancel(cancelled)
    print(queue.run_all())
    print("-" * 40)

    print("Task 3")
    database = FakeDatabase()
    transaction = Transaction()
    transaction.add(InsertCommand(database, {"id": 1, "name": "Анна"}))
    transaction.add(UpdateCommand(database, 1, {"name": "Иван"}))
    transaction.commit()
    print(database.rows)
    transaction.rollback()
    print(database.rows)
    print("-" * 40)

    print("Task 4")
    remote = SmartRemote()
    light = Light()
    fan = Fan()
    remote.set_command(0, HomeCommand(light, "on"), HomeCommand(light, "off"))
    remote.set_command(1, HomeCommand(fan, "on"), HomeCommand(fan, "off"))
    remote.press_on(0)
    remote.press_off(1)
    remote.undo()
    remote.macro(MacroCommand([HomeCommand(light, "on"), HomeCommand(SecuritySystem(), "on")]))
    print("-" * 40)

    print("Task 5")
    scheduler = Scheduler(retries=1)
    scheduler.run(
        [
            BackupCommand("backup"),
            CleanupCommand("cleanup", fail_once=True),
            SyncCommand("sync"),
        ]
    )
    print(scheduler.log.entries)

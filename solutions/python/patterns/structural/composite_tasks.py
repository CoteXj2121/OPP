from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# Task 1
class FileSystemNode(ABC):
    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def print_tree(self, indent: int = 0) -> list[str]:
        pass

    @abstractmethod
    def search(self, name: str) -> list[str]:
        pass


@dataclass
class File(FileSystemNode):
    name: str
    size: int

    def get_size(self) -> int:
        return self.size

    def print_tree(self, indent: int = 0) -> list[str]:
        return [" " * indent + self.name]

    def search(self, name: str) -> list[str]:
        return [self.name] if name in self.name else []


@dataclass
class Directory(FileSystemNode):
    name: str
    children: list[FileSystemNode] = field(default_factory=list)

    def add(self, node: FileSystemNode) -> None:
        self.children.append(node)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)

    def print_tree(self, indent: int = 0) -> list[str]:
        lines = [" " * indent + f"[{self.name}]"]
        for child in self.children:
            lines.extend(child.print_tree(indent + 2))
        return lines

    def search(self, name: str) -> list[str]:
        results = [self.name] if name in self.name else []
        for child in self.children:
            results.extend(child.search(name))
        return results


# Task 2
class CartItem(ABC):
    @abstractmethod
    def total_price(self) -> float:
        pass

    @abstractmethod
    def describe(self, indent: int = 0) -> list[str]:
        pass


@dataclass
class Product(CartItem):
    name: str
    price: float
    quantity: int

    def total_price(self) -> float:
        return self.price * self.quantity

    def describe(self, indent: int = 0) -> list[str]:
        return [" " * indent + f"{self.name}: {self.total_price()}"]


@dataclass
class Bundle(CartItem):
    name: str
    discount_percent: float = 0
    items: list[CartItem] = field(default_factory=list)

    def add(self, item: CartItem) -> None:
        self.items.append(item)

    def total_price(self) -> float:
        subtotal = sum(item.total_price() for item in self.items)
        return subtotal * (1 - self.discount_percent / 100)

    def describe(self, indent: int = 0) -> list[str]:
        lines = [" " * indent + f"{self.name}: {self.total_price()}"]
        for item in self.items:
            lines.extend(item.describe(indent + 2))
        return lines


# Task 3
class OrgUnit(ABC):
    @abstractmethod
    def get_salary_budget(self) -> float:
        pass

    @abstractmethod
    def get_headcount(self) -> int:
        pass

    @abstractmethod
    def print_structure(self, indent: int = 0) -> list[str]:
        pass


@dataclass
class Employee(OrgUnit):
    name: str
    position: str
    salary: float

    def get_salary_budget(self) -> float:
        return self.salary

    def get_headcount(self) -> int:
        return 1

    def print_structure(self, indent: int = 0) -> list[str]:
        return [" " * indent + f"{self.name} ({self.position})"]


@dataclass
class Department(OrgUnit):
    name: str
    children: list[OrgUnit] = field(default_factory=list)

    def add(self, item: OrgUnit) -> None:
        self.children.append(item)

    def get_salary_budget(self) -> float:
        return sum(child.get_salary_budget() for child in self.children)

    def get_headcount(self) -> int:
        return sum(child.get_headcount() for child in self.children)

    def print_structure(self, indent: int = 0) -> list[str]:
        lines = [" " * indent + f"Отдел: {self.name}"]
        for child in self.children:
            lines.extend(child.print_structure(indent + 2))
        return lines


# Task 4
class MenuComponent(ABC):
    @abstractmethod
    def print_menu(self, indent: int = 0) -> list[str]:
        pass

    @abstractmethod
    def get_total_items(self) -> int:
        pass

    @abstractmethod
    def filter_vegetarian(self):
        pass


@dataclass
class MenuItem(MenuComponent):
    name: str
    description: str
    price: float
    vegetarian: bool

    def print_menu(self, indent: int = 0) -> list[str]:
        mark = " (veg)" if self.vegetarian else ""
        return [" " * indent + f"{self.name}{mark} - {self.price}"]

    def get_total_items(self) -> int:
        return 1

    def filter_vegetarian(self):
        return self if self.vegetarian else None


@dataclass
class MenuSection(MenuComponent):
    name: str
    children: list[MenuComponent] = field(default_factory=list)

    def add(self, component: MenuComponent) -> None:
        self.children.append(component)

    def print_menu(self, indent: int = 0) -> list[str]:
        lines = [" " * indent + f"[{self.name}]"]
        for child in self.children:
            lines.extend(child.print_menu(indent + 2))
        return lines

    def get_total_items(self) -> int:
        return sum(child.get_total_items() for child in self.children)

    def filter_vegetarian(self):
        filtered = MenuSection(self.name)
        for child in self.children:
            result = child.filter_vegetarian()
            if result is not None:
                filtered.add(result)
        return filtered if filtered.children else None


# Task 5
class WorkItem(ABC):
    @abstractmethod
    def get_progress(self) -> float:
        pass

    @abstractmethod
    def get_total_hours(self) -> int:
        pass

    @abstractmethod
    def find_by_assignee(self, name: str) -> list[str]:
        pass


@dataclass
class Task(WorkItem):
    name: str
    assignee: str
    hours: int
    status: str

    def get_progress(self) -> float:
        return 100.0 if self.status == "done" else 0.0

    def get_total_hours(self) -> int:
        return self.hours

    def find_by_assignee(self, name: str) -> list[str]:
        return [self.name] if self.assignee == name else []

    def count_tasks(self) -> tuple[int, int]:
        return (1, 1) if self.status == "done" else (0, 1)


@dataclass
class Epic(WorkItem):
    name: str
    items: list[WorkItem] = field(default_factory=list)

    def add(self, item: WorkItem) -> None:
        self.items.append(item)

    def _task_stats(self) -> tuple[int, int]:
        completed = 0
        total = 0
        for item in self.items:
            if isinstance(item, Task):
                done, all_count = item.count_tasks()
            else:
                done, all_count = item._task_stats()
            completed += done
            total += all_count
        return completed, total

    def get_progress(self) -> float:
        completed, total = self._task_stats()
        return 0.0 if total == 0 else completed / total * 100

    def get_total_hours(self) -> int:
        return sum(item.get_total_hours() for item in self.items)

    def find_by_assignee(self, name: str) -> list[str]:
        results: list[str] = []
        for item in self.items:
            results.extend(item.find_by_assignee(name))
        return results


if __name__ == "__main__":
    print("Task 1")
    root = Directory("root")
    root.add(File("notes.txt", 10))
    images = Directory("images")
    images.add(File("cat.png", 120))
    images.add(File("dog.png", 140))
    root.add(images)
    print(root.get_size())
    print(root.print_tree())
    print(root.search("cat"))
    print("-" * 40)

    print("Task 2")
    bundle = Bundle("Набор", discount_percent=10)
    bundle.add(Product("Книга", 350, 2))
    sub_bundle = Bundle("Канцелярия")
    sub_bundle.add(Product("Ручка", 50, 3))
    bundle.add(sub_bundle)
    print(bundle.total_price())
    print(bundle.describe())
    print("-" * 40)

    print("Task 3")
    dev = Department("Разработка")
    dev.add(Employee("Анна", "Backend", 120000))
    dev.add(Employee("Иван", "Frontend", 110000))
    company = Department("Компания")
    company.add(dev)
    print(company.get_salary_budget())
    print(company.get_headcount())
    print(company.print_structure())
    print("-" * 40)

    print("Task 4")
    menu = MenuSection("Меню")
    menu.add(MenuItem("Салат", "Свежий", 250, True))
    hot = MenuSection("Горячее")
    hot.add(MenuItem("Паста", "С сыром", 450, True))
    hot.add(MenuItem("Стейк", "Говядина", 900, False))
    menu.add(hot)
    print(menu.print_menu())
    veg = menu.filter_vegetarian()
    print(veg.print_menu() if veg else [])
    print("-" * 40)

    print("Task 5")
    sprint = Epic("Sprint 1")
    sprint.add(Task("API", "Алексей", 8, "done"))
    sprint.add(Task("UI", "Мария", 6, "in_progress"))
    print(sprint.get_progress())
    print(sprint.get_total_hours())
    print(sprint.find_by_assignee("Алексей"))

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


# Task 1
@dataclass
class TreeNode:
    value: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


class InOrderIterator:
    def __init__(self, root: TreeNode | None):
        self.stack: list[TreeNode] = []
        self._push_left(root)

    def _push_left(self, node: TreeNode | None) -> None:
        while node is not None:
            self.stack.append(node)
            node = node.left

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if not self.stack:
            raise StopIteration
        node = self.stack.pop()
        self._push_left(node.right)
        return node.value


class PreOrderIterator:
    def __init__(self, root: TreeNode | None):
        self.stack = [root] if root else []

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if not self.stack:
            raise StopIteration
        node = self.stack.pop()
        if node.right:
            self.stack.append(node.right)
        if node.left:
            self.stack.append(node.left)
        return node.value


class PostOrderIterator:
    def __init__(self, root: TreeNode | None):
        self.values = self._collect(root)
        self.index = 0

    def _collect(self, node: TreeNode | None) -> list[int]:
        if node is None:
            return []
        return self._collect(node.left) + self._collect(node.right) + [node.value]

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.index >= len(self.values):
            raise StopIteration
        value = self.values[self.index]
        self.index += 1
        return value


# Task 2
class FlatIterator:
    def __init__(self, nested):
        self.stack = [iter(nested)]

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            try:
                item = next(self.stack[-1])
                if isinstance(item, list):
                    self.stack.append(iter(item))
                else:
                    return item
            except StopIteration:
                self.stack.pop()
        raise StopIteration


# Task 3
class FilterIterator:
    def __init__(self, iterable, predicate):
        self.iterator = iter(iterable)
        self.predicate = predicate

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            item = next(self.iterator)
            if self.predicate(item):
                return item


class MapIterator:
    def __init__(self, iterable, mapper):
        self.iterator = iter(iterable)
        self.mapper = mapper

    def __iter__(self):
        return self

    def __next__(self):
        return self.mapper(next(self.iterator))


# Task 4
class PaginatedIterator:
    def __init__(self, fetch_page, size: int):
        self.fetch_page = fetch_page
        self.size = size
        self.page = 1
        self.items: list = []
        self.index = 0
        self.finished = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.finished:
            raise StopIteration
        if self.index >= len(self.items):
            self.items = self.fetch_page(self.page, self.size)
            self.page += 1
            self.index = 0
            if not self.items:
                self.finished = True
                raise StopIteration
        item = self.items[self.index]
        self.index += 1
        return item


# Task 5
class Graph:
    def __init__(self):
        self.edges: dict[str, list[str]] = {}

    def add_edge(self, source: str, target: str) -> None:
        self.edges.setdefault(source, []).append(target)
        self.edges.setdefault(target, [])


class BFSIterator:
    def __init__(self, graph: Graph, start: str):
        self.graph = graph
        self.queue = deque([start])
        self.visited = set()

    def __iter__(self):
        return self

    def __next__(self):
        while self.queue:
            vertex = self.queue.popleft()
            if vertex in self.visited:
                continue
            self.visited.add(vertex)
            for neighbor in self.graph.edges.get(vertex, []):
                if neighbor not in self.visited:
                    self.queue.append(neighbor)
            return vertex
        raise StopIteration


class DFSIterator:
    def __init__(self, graph: Graph, start: str):
        self.graph = graph
        self.stack = [start]
        self.visited = set()

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            vertex = self.stack.pop()
            if vertex in self.visited:
                continue
            self.visited.add(vertex)
            for neighbor in reversed(self.graph.edges.get(vertex, [])):
                if neighbor not in self.visited:
                    self.stack.append(neighbor)
            return vertex
        raise StopIteration


if __name__ == "__main__":
    print("Task 1")
    root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6, TreeNode(5), TreeNode(7)))
    print(list(InOrderIterator(root)))
    print(list(PreOrderIterator(root)))
    print(list(PostOrderIterator(root)))
    print("-" * 40)

    print("Task 2")
    print(list(FlatIterator([1, [2, [3, 4]], 5])))
    print("-" * 40)

    print("Task 3")
    users = [{"name": "Анна", "active": True}, {"name": "Иван", "active": False}, {"name": "Мария", "active": True}]
    active_names = MapIterator(FilterIterator(users, lambda user: user["active"]), lambda user: user["name"])
    print(list(active_names))
    print("-" * 40)

    print("Task 4")
    data = list(range(1, 8))

    def fetch_page(page: int, size: int):
        start = (page - 1) * size
        return data[start : start + size]

    print(list(PaginatedIterator(fetch_page, 3)))
    print("-" * 40)

    print("Task 5")
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")
    print(list(BFSIterator(graph, "A")))
    print(list(DFSIterator(graph, "A")))

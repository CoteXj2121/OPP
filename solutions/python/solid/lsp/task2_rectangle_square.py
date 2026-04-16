from abc import ABC, abstractmethod


class BadRectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def set_width(self, width: float) -> None:
        self.width = width

    def set_height(self, height: float) -> None:
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class BadSquare(BadRectangle):
    def set_width(self, width: float) -> None:
        self.width = width
        self.height = width

    def set_height(self, height: float) -> None:
        self.width = height
        self.height = height


def print_bad_area(shape: BadRectangle) -> None:
    shape.set_width(5)
    shape.set_height(10)
    print(f"Проблемный результат: {shape.area()}")


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Square(Shape):
    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return self.side * self.side


if __name__ == "__main__":
    print_bad_area(BadRectangle(2, 3))
    print_bad_area(BadSquare(2, 2))

    shapes: list[Shape] = [Rectangle(5, 10), Square(5)]
    for shape in shapes:
        print(f"Корректная площадь: {shape.area()}")

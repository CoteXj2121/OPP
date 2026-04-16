from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius**2


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height


class AreaCalculator:
    def calculate(self, shape: Shape) -> float:
        return shape.area()


if __name__ == "__main__":
    calculator = AreaCalculator()

    print(calculator.calculate(Circle(5)))
    print(calculator.calculate(Rectangle(4, 6)))
    print(calculator.calculate(Triangle(8, 3)))

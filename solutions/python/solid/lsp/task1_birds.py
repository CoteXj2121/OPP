from abc import ABC, abstractmethod


class Bird(ABC):
    @abstractmethod
    def describe(self) -> str:
        pass


class FlyingBird(Bird):
    @abstractmethod
    def fly(self) -> str:
        pass


class Sparrow(FlyingBird):
    def describe(self) -> str:
        return "Воробей"

    def fly(self) -> str:
        return "Воробей летит"


class Eagle(FlyingBird):
    def describe(self) -> str:
        return "Орел"

    def fly(self) -> str:
        return "Орел парит в небе"


class Penguin(Bird):
    def describe(self) -> str:
        return "Пингвин"

    def swim(self) -> str:
        return "Пингвин плывет"


def make_birds_fly(birds: list[FlyingBird]) -> None:
    for bird in birds:
        print(bird.fly())


if __name__ == "__main__":
    make_birds_fly([Sparrow(), Eagle()])

    penguin = Penguin()
    print(penguin.describe())
    print(penguin.swim())

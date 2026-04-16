from abc import ABC, abstractmethod


class Workable(ABC):
    @abstractmethod
    def work(self) -> None:
        pass


class Eatable(ABC):
    @abstractmethod
    def eat(self) -> None:
        pass


class HumanWorker(Workable, Eatable):
    def work(self) -> None:
        print("Человек работает")

    def eat(self) -> None:
        print("Человек обедает")


class RobotWorker(Workable):
    def work(self) -> None:
        print("Робот работает")


def manage(workers: list[Workable]) -> None:
    for worker in workers:
        worker.work()


def lunch_break(workers: list[Eatable]) -> None:
    for worker in workers:
        worker.eat()


if __name__ == "__main__":
    human = HumanWorker()
    robot = RobotWorker()

    manage([human, robot])
    lunch_break([human])

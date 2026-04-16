from abc import ABC, abstractmethod


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        pass


class BubbleSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        arr = data[:]
        for i in range(len(arr)):
            for j in range(len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class BuiltinSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        return sorted(data)


class SelectionSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        arr = data[:]
        for i in range(len(arr)):
            min_index = i
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[min_index]:
                    min_index = j
            arr[i], arr[min_index] = arr[min_index], arr[i]
        return arr


class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        return self.strategy.sort(data)


if __name__ == "__main__":
    numbers = [5, 3, 8, 1, 9, 2]

    print(Sorter(BubbleSort()).sort(numbers))
    print(Sorter(BuiltinSort()).sort(numbers))
    print(Sorter(SelectionSort()).sort(numbers))

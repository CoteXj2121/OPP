from abc import ABC, abstractmethod


class FindableRepository(ABC):
    @abstractmethod
    def find(self, entity_id: int) -> dict:
        pass


class SavableRepository(ABC):
    @abstractmethod
    def save(self, entity: dict) -> None:
        pass


class DeletableRepository(ABC):
    @abstractmethod
    def delete(self, entity_id: int) -> None:
        pass


class CsvExportable(ABC):
    @abstractmethod
    def export_csv(self) -> str:
        pass


class UserRepository(
    FindableRepository, SavableRepository, DeletableRepository, CsvExportable
):
    def find(self, entity_id: int) -> dict:
        return {"id": entity_id, "name": "Анна"}

    def save(self, entity: dict) -> None:
        print(f"Сохранение: {entity}")

    def delete(self, entity_id: int) -> None:
        print(f"Удаление id={entity_id}")

    def export_csv(self) -> str:
        return "id,name\n1,Анна"


class ReadOnlyRepository(FindableRepository):
    def find(self, entity_id: int) -> dict:
        return {"id": entity_id, "name": "Иван"}


if __name__ == "__main__":
    read_only_repo = ReadOnlyRepository()
    print(read_only_repo.find(1))

    user_repo = UserRepository()
    user_repo.save({"name": "Новый"})
    print(user_repo.export_csv())

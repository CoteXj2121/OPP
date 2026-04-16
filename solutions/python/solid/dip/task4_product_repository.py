from abc import ABC, abstractmethod


class DatabaseConnection(ABC):
    @abstractmethod
    def query(self, sql: str) -> list[dict]:
        pass


class MySQLConnection(DatabaseConnection):
    def query(self, sql: str) -> list[dict]:
        print(f"[MySQL] Выполнение: {sql}")
        return [{"id": 1, "name": "Товар A"}]


class PostgreSQLConnection(DatabaseConnection):
    def query(self, sql: str) -> list[dict]:
        print(f"[PostgreSQL] Выполнение: {sql}")
        return [{"id": 2, "name": "Товар B"}]


class ProductRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def find_all(self) -> list[dict]:
        return self.db.query("SELECT * FROM products")

    def find_by_id(self, product_id: int) -> dict:
        results = self.db.query(f"SELECT * FROM products WHERE id = {product_id}")
        return results[0] if results else {}


if __name__ == "__main__":
    mysql_repo = ProductRepository(MySQLConnection())
    postgres_repo = ProductRepository(PostgreSQLConnection())

    print(mysql_repo.find_all())
    print(postgres_repo.find_by_id(2))

from __future__ import annotations

from abc import ABC, abstractmethod


class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self) -> str:
        pass

    @abstractmethod
    def query(self, sql: str) -> str:
        pass

    @abstractmethod
    def disconnect(self) -> str:
        pass


class MySQLConnection(DatabaseConnection):
    def connect(self) -> str:
        return "Подключение к MySQL"

    def query(self, sql: str) -> str:
        return f"MySQL выполняет запрос: {sql}"

    def disconnect(self) -> str:
        return "Отключение от MySQL"


class PostgreSQLConnection(DatabaseConnection):
    def connect(self) -> str:
        return "Подключение к PostgreSQL"

    def query(self, sql: str) -> str:
        return f"PostgreSQL выполняет запрос: {sql}"

    def disconnect(self) -> str:
        return "Отключение от PostgreSQL"


class SQLiteConnection(DatabaseConnection):
    def connect(self) -> str:
        return "Подключение к SQLite"

    def query(self, sql: str) -> str:
        return f"SQLite выполняет запрос: {sql}"

    def disconnect(self) -> str:
        return "Отключение от SQLite"


class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self) -> DatabaseConnection:
        pass

    def run_query(self, sql: str) -> list[str]:
        connection = self.create_connection()
        return [
            connection.connect(),
            connection.query(sql),
            connection.disconnect(),
        ]


class MySQLFactory(DatabaseFactory):
    def create_connection(self) -> DatabaseConnection:
        return MySQLConnection()


class PostgreSQLFactory(DatabaseFactory):
    def create_connection(self) -> DatabaseConnection:
        return PostgreSQLConnection()


class SQLiteFactory(DatabaseFactory):
    def create_connection(self) -> DatabaseConnection:
        return SQLiteConnection()


if __name__ == "__main__":
    query = "SELECT * FROM users"

    for factory in (MySQLFactory(), PostgreSQLFactory(), SQLiteFactory()):
        for step in factory.run_query(query):
            print(step)
        print("-" * 30)

from abc import ABC, abstractmethod


class Cache(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value) -> None:
        pass


class RedisCache(Cache):
    def __init__(self):
        self._store: dict[str, dict] = {}

    def get(self, key: str):
        return self._store.get(key)

    def set(self, key: str, value) -> None:
        self._store[key] = value
        print(f"[Redis] Сохранено: {key}")


class InMemoryCache(Cache):
    def __init__(self):
        self._store: dict[str, dict] = {}

    def get(self, key: str):
        return self._store.get(key)

    def set(self, key: str, value) -> None:
        self._store[key] = value
        print(f"[Memory] Сохранено: {key}")


class ArticleService:
    def __init__(self, cache: Cache):
        self.cache = cache

    def get_article(self, article_id: int) -> dict:
        key = f"article:{article_id}"
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        article = {"id": article_id, "title": f"Статья #{article_id}"}
        self.cache.set(key, article)
        return article


if __name__ == "__main__":
    redis_service = ArticleService(RedisCache())
    memory_service = ArticleService(InMemoryCache())

    print(redis_service.get_article(1))
    print(redis_service.get_article(1))
    print(memory_service.get_article(2))

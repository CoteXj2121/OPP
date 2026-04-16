from abc import ABC, abstractmethod


class Account:
    def __init__(self, name: str):
        self.name = name


class DiscountableAccount(Account, ABC):
    @abstractmethod
    def get_discount(self) -> float:
        pass


class UserAccount(DiscountableAccount):
    def get_discount(self) -> float:
        return 0.10


class PremiumAccount(DiscountableAccount):
    def get_discount(self) -> float:
        return 0.25


class GuestAccount(Account):
    pass


def print_discounts(accounts: list[DiscountableAccount]) -> None:
    for account in accounts:
        print(f"{account.name}: скидка {account.get_discount() * 100}%")


if __name__ == "__main__":
    print_discounts([UserAccount("Анна"), PremiumAccount("Иван")])

    guest = GuestAccount("Гость")
    print(f"{guest.name}: скидка недоступна")

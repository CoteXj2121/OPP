class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class EmailValidator:
    def is_valid(self, email: str) -> bool:
        if "@" not in email:
            return False
        domain = email.split("@", maxsplit=1)[1]
        return "." in domain


class WelcomeEmailSender:
    def send(self, user: User) -> None:
        print(f"Отправка письма на {user.email}: Добро пожаловать, {user.name}!")


if __name__ == "__main__":
    user = User("Алексей", "alexey@example.com")
    validator = EmailValidator()
    sender = WelcomeEmailSender()

    if validator.is_valid(user.email):
        sender.send(user)
    else:
        print("Некорректный email")

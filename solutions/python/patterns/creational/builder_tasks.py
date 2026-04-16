from __future__ import annotations

from dataclasses import dataclass, field


# Task 1
@dataclass
class Resume:
    name: str = ""
    contacts: dict[str, str] = field(default_factory=dict)
    experience: list[str] = field(default_factory=list)
    education: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)


class ResumeBuilder:
    def __init__(self):
        self._resume = Resume()

    def set_name(self, name: str) -> ResumeBuilder:
        self._resume.name = name
        return self

    def set_contacts(self, **contacts: str) -> ResumeBuilder:
        self._resume.contacts = contacts
        return self

    def add_experience(self, experience: str) -> ResumeBuilder:
        self._resume.experience.append(experience)
        return self

    def add_education(self, education: str) -> ResumeBuilder:
        self._resume.education.append(education)
        return self

    def add_skill(self, skill: str) -> ResumeBuilder:
        self._resume.skills.append(skill)
        return self

    def build(self) -> Resume:
        resume = self._resume
        self._resume = Resume()
        return resume


class ResumeDirector:
    def build_standard_resume(self) -> Resume:
        return (
            ResumeBuilder()
            .set_name("Алексей")
            .set_contacts(email="alexey@example.com", phone="+79990000000")
            .add_experience("Стажер Python")
            .add_education("УрФУ")
            .add_skill("Python")
            .build()
        )

    def build_extended_resume(self) -> Resume:
        return (
            ResumeBuilder()
            .set_name("Мария")
            .set_contacts(email="maria@example.com", telegram="@maria")
            .add_experience("Backend Developer")
            .add_experience("Team Lead")
            .add_education("ИТМО")
            .add_skill("Python")
            .add_skill("SQL")
            .add_skill("Docker")
            .build()
        )


# Task 2
@dataclass
class HttpRequest:
    method: str
    url: str
    headers: dict[str, str]
    body: str | None
    timeout: int


class HttpRequestBuilder:
    def __init__(self):
        self._method = "GET"
        self._url = ""
        self._headers: dict[str, str] = {}
        self._body: str | None = None
        self._timeout = 30

    def set_method(self, method: str) -> HttpRequestBuilder:
        self._method = method
        return self

    def set_url(self, url: str) -> HttpRequestBuilder:
        self._url = url
        return self

    def add_header(self, key: str, value: str) -> HttpRequestBuilder:
        self._headers[key] = value
        return self

    def set_body(self, body: str) -> HttpRequestBuilder:
        self._body = body
        return self

    def set_timeout(self, timeout: int) -> HttpRequestBuilder:
        self._timeout = timeout
        return self

    def build(self) -> HttpRequest:
        return HttpRequest(
            method=self._method,
            url=self._url,
            headers=dict(self._headers),
            body=self._body,
            timeout=self._timeout,
        )


class HttpRequestDirector:
    def build_json_post(self, url: str, body: str) -> HttpRequest:
        return (
            HttpRequestBuilder()
            .set_method("POST")
            .set_url(url)
            .add_header("Content-Type", "application/json")
            .set_body(body)
            .build()
        )

    def build_auth_get(self, url: str, token: str) -> HttpRequest:
        return (
            HttpRequestBuilder()
            .set_method("GET")
            .set_url(url)
            .add_header("Authorization", f"Bearer {token}")
            .build()
        )

    def build_multipart_upload(self, url: str, filename: str) -> HttpRequest:
        return (
            HttpRequestBuilder()
            .set_method("POST")
            .set_url(url)
            .add_header("Content-Type", "multipart/form-data")
            .set_body(f"file={filename}")
            .set_timeout(120)
            .build()
        )


# Task 3
@dataclass
class Pizza:
    size: str
    dough: str
    sauce: str
    cheese: str
    toppings: list[str]


class PizzaBuilder:
    def __init__(self):
        self._size: str | None = None
        self._dough: str | None = None
        self._sauce = "томатный"
        self._cheese = "моцарелла"
        self._toppings: list[str] = []

    def set_size(self, size: str) -> PizzaBuilder:
        self._size = size
        return self

    def set_dough(self, dough: str) -> PizzaBuilder:
        self._dough = dough
        return self

    def set_sauce(self, sauce: str) -> PizzaBuilder:
        self._sauce = sauce
        return self

    def set_cheese(self, cheese: str) -> PizzaBuilder:
        self._cheese = cheese
        return self

    def add_topping(self, topping: str) -> PizzaBuilder:
        self._toppings.append(topping)
        return self

    def build(self) -> Pizza:
        if self._size is None or self._dough is None:
            raise ValueError("Размер и тесто обязательны")
        return Pizza(
            size=self._size,
            dough=self._dough,
            sauce=self._sauce,
            cheese=self._cheese,
            toppings=list(self._toppings),
        )


class PizzaDirector:
    def build_margherita(self) -> Pizza:
        return (
            PizzaBuilder()
            .set_size("medium")
            .set_dough("thin")
            .set_sauce("томатный")
            .set_cheese("моцарелла")
            .add_topping("базилик")
            .build()
        )

    def build_pepperoni(self) -> Pizza:
        return (
            PizzaBuilder()
            .set_size("large")
            .set_dough("classic")
            .add_topping("пепперони")
            .add_topping("оливки")
            .build()
        )

    def build_vegetarian(self) -> Pizza:
        return (
            PizzaBuilder()
            .set_size("medium")
            .set_dough("wholegrain")
            .add_topping("помидоры")
            .add_topping("грибы")
            .add_topping("перец")
            .build()
        )


# Task 4
class SelectQueryBuilder:
    def __init__(self):
        self._table = ""
        self._fields: list[str] = []
        self._where: list[str] = []
        self._joins: list[str] = []
        self._order_by = ""
        self._limit: int | None = None
        self._offset: int | None = None

    def from_(self, table: str) -> SelectQueryBuilder:
        self._table = table
        return self

    def select(self, *fields: str) -> SelectQueryBuilder:
        self._fields.extend(fields)
        return self

    def where(self, condition: str) -> SelectQueryBuilder:
        self._where.append(condition)
        return self

    def join(self, expression: str) -> SelectQueryBuilder:
        self._joins.append(expression)
        return self

    def order_by(self, expression: str) -> SelectQueryBuilder:
        self._order_by = expression
        return self

    def limit(self, value: int) -> SelectQueryBuilder:
        self._limit = value
        return self

    def offset(self, value: int) -> SelectQueryBuilder:
        self._offset = value
        return self

    def build(self) -> str:
        if not self._table:
            raise ValueError("Таблица не указана")
        fields = ", ".join(self._fields) if self._fields else "*"
        parts = [f"SELECT {fields} FROM {self._table}"]
        parts.extend(self._joins)
        if self._where:
            parts.append("WHERE " + " AND ".join(self._where))
        if self._order_by:
            parts.append(f"ORDER BY {self._order_by}")
        if self._limit is not None:
            parts.append(f"LIMIT {self._limit}")
        if self._offset is not None:
            parts.append(f"OFFSET {self._offset}")
        return " ".join(parts) + ";"


# Task 5
@dataclass
class EmailMessage:
    from_address: str
    to: list[str]
    cc: list[str]
    bcc: list[str]
    subject: str
    text_body: str | None
    html_body: str | None
    attachments: list[str]


class EmailBuilder:
    def __init__(self):
        self._from_address = ""
        self._to: list[str] = []
        self._cc: list[str] = []
        self._bcc: list[str] = []
        self._subject = ""
        self._text_body: str | None = None
        self._html_body: str | None = None
        self._attachments: list[str] = []

    def set_from(self, address: str) -> EmailBuilder:
        self._from_address = address
        return self

    def add_to(self, address: str) -> EmailBuilder:
        self._to.append(address)
        return self

    def add_cc(self, address: str) -> EmailBuilder:
        self._cc.append(address)
        return self

    def add_bcc(self, address: str) -> EmailBuilder:
        self._bcc.append(address)
        return self

    def set_subject(self, subject: str) -> EmailBuilder:
        self._subject = subject
        return self

    def set_text_body(self, body: str) -> EmailBuilder:
        self._text_body = body
        return self

    def set_html_body(self, body: str) -> EmailBuilder:
        self._html_body = body
        return self

    def add_attachment(self, filename: str) -> EmailBuilder:
        self._attachments.append(filename)
        return self

    def build(self) -> EmailMessage:
        if not self._from_address:
            raise ValueError("Не указан отправитель")
        if not self._to:
            raise ValueError("Не указан получатель")
        if not self._subject:
            raise ValueError("Не указана тема")
        return EmailMessage(
            from_address=self._from_address,
            to=list(self._to),
            cc=list(self._cc),
            bcc=list(self._bcc),
            subject=self._subject,
            text_body=self._text_body,
            html_body=self._html_body,
            attachments=list(self._attachments),
        )


class EmailDirector:
    def build_welcome_email(self, recipient: str) -> EmailMessage:
        return (
            EmailBuilder()
            .set_from("support@example.com")
            .add_to(recipient)
            .set_subject("Добро пожаловать")
            .set_text_body("Спасибо за регистрацию")
            .build()
        )

    def build_password_reset_email(self, recipient: str, token: str) -> EmailMessage:
        return (
            EmailBuilder()
            .set_from("security@example.com")
            .add_to(recipient)
            .set_subject("Сброс пароля")
            .set_text_body(f"Ваш код: {token}")
            .add_attachment("instruction.pdf")
            .build()
        )


if __name__ == "__main__":
    director = ResumeDirector()
    print("Task 1")
    print(director.build_standard_resume())
    print(director.build_extended_resume())
    print("-" * 40)

    request_director = HttpRequestDirector()
    print("Task 2")
    print(request_director.build_json_post("https://api.example.com", '{"ok": true}'))
    print(request_director.build_auth_get("https://api.example.com/users", "token-123"))
    print(request_director.build_multipart_upload("https://upload.example.com", "photo.png"))
    print("-" * 40)

    pizza_director = PizzaDirector()
    print("Task 3")
    print(pizza_director.build_margherita())
    print(pizza_director.build_pepperoni())
    print(pizza_director.build_vegetarian())
    print("-" * 40)

    print("Task 4")
    query = (
        SelectQueryBuilder()
        .select("users.id", "users.name")
        .from_("users")
        .join("LEFT JOIN orders ON orders.user_id = users.id")
        .where("users.active = 1")
        .order_by("users.name ASC")
        .limit(10)
        .offset(20)
        .build()
    )
    print(query)
    print("-" * 40)

    email_director = EmailDirector()
    print("Task 5")
    print(email_director.build_welcome_email("user@example.com"))
    print(email_director.build_password_reset_email("user@example.com", "ABC123"))

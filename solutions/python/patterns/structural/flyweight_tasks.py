from __future__ import annotations

from dataclasses import dataclass, field


# Task 1
@dataclass(frozen=True)
class TreeType:
    name: str
    texture: str
    color: str


@dataclass
class Tree:
    x: int
    y: int
    size: int
    tree_type: TreeType


class TreeFactory:
    def __init__(self):
        self._types: dict[tuple[str, str, str], TreeType] = {}

    def get_type(self, name: str, texture: str, color: str) -> TreeType:
        key = (name, texture, color)
        if key not in self._types:
            self._types[key] = TreeType(name, texture, color)
        return self._types[key]

    def count_types(self) -> int:
        return len(self._types)


# Task 2
@dataclass(frozen=True)
class CharacterStyle:
    font: str
    size: int
    color: str
    bold: bool
    italic: bool


@dataclass
class Character:
    symbol: str
    position: int
    style: CharacterStyle


class StyleFactory:
    def __init__(self):
        self._styles: dict[tuple[str, int, str, bool, bool], CharacterStyle] = {}

    def get_style(self, font: str, size: int, color: str, bold: bool, italic: bool) -> CharacterStyle:
        key = (font, size, color, bold, italic)
        if key not in self._styles:
            self._styles[key] = CharacterStyle(font, size, color, bold, italic)
        return self._styles[key]

    def count_styles(self) -> int:
        return len(self._styles)


# Task 3
@dataclass(frozen=True)
class BulletType:
    name: str
    model: str
    texture: str
    damage: int
    sound: str


@dataclass
class Bullet:
    x: float
    y: float
    speed: float
    direction: float
    bullet_type: BulletType


class BulletFactory:
    def __init__(self):
        self._types: dict[str, BulletType] = {}

    def get_type(self, name: str, model: str, texture: str, damage: int, sound: str) -> BulletType:
        if name not in self._types:
            self._types[name] = BulletType(name, model, texture, damage, sound)
        return self._types[name]

    def count_types(self) -> int:
        return len(self._types)


# Task 4
@dataclass(frozen=True)
class FileIcon:
    extension: str
    image: str
    color: str


@dataclass
class FileEntry:
    name: str
    path: str
    size: int
    date: str
    icon: FileIcon


class IconRegistry:
    def __init__(self):
        self._icons: dict[str, FileIcon] = {}

    def get_icon(self, extension: str, image: str, color: str) -> FileIcon:
        if extension not in self._icons:
            self._icons[extension] = FileIcon(extension, image, color)
        return self._icons[extension]

    def count_icons(self) -> int:
        return len(self._icons)


# Task 5
@dataclass(frozen=True)
class ParticleType:
    name: str
    texture: str
    color: str
    behavior: str


@dataclass
class Particle:
    x: float
    y: float
    velocity_x: float
    velocity_y: float
    lifetime: float
    particle_type: ParticleType


class ParticleFactory:
    def __init__(self):
        self._types: dict[str, ParticleType] = {}

    def get_type(self, name: str, texture: str, color: str, behavior: str) -> ParticleType:
        if name not in self._types:
            self._types[name] = ParticleType(name, texture, color, behavior)
        return self._types[name]


class ParticleSystem:
    def __init__(self, factory: ParticleFactory):
        self.factory = factory
        self.particles: list[Particle] = []

    def emit(self, type_name: str, x: float, y: float) -> None:
        configs = {
            "spark": ("spark.png", "orange", "fast"),
            "smoke": ("smoke.png", "gray", "slow"),
            "snow": ("snow.png", "white", "fall"),
        }
        texture, color, behavior = configs[type_name]
        particle_type = self.factory.get_type(type_name, texture, color, behavior)
        self.particles.append(Particle(x, y, 1.0, 1.5, 5.0, particle_type))

    def update(self, dt: float) -> None:
        alive: list[Particle] = []
        for particle in self.particles:
            particle.x += particle.velocity_x * dt
            particle.y += particle.velocity_y * dt
            particle.lifetime -= dt
            if particle.lifetime > 0:
                alive.append(particle)
        self.particles = alive

    def render(self) -> list[str]:
        return [
            f"{particle.particle_type.name} at ({particle.x:.1f}, {particle.y:.1f})"
            for particle in self.particles
        ]


if __name__ == "__main__":
    print("Task 1")
    tree_factory = TreeFactory()
    trees = [Tree(i, i * 2, 10, tree_factory.get_type("oak", "oak.png", "green")) for i in range(1000)]
    print(len(trees), tree_factory.count_types())
    print("-" * 40)

    print("Task 2")
    style_factory = StyleFactory()
    style = style_factory.get_style("Arial", 14, "black", False, False)
    chars = [Character(letter, index, style) for index, letter in enumerate("Hello world")]
    print(len(chars), style_factory.count_styles())
    print("-" * 40)

    print("Task 3")
    bullet_factory = BulletFactory()
    bullets = []
    for bullet_index in range(10000):
        bullet_type = bullet_factory.get_type(f"type-{bullet_index % 5}", "model", "texture", 10, "boom")
        bullets.append(Bullet(0, 0, 20, 90, bullet_type))
    print(len(bullets), bullet_factory.count_types())
    print("-" * 40)

    print("Task 4")
    registry = IconRegistry()
    files = [
        FileEntry("report.pdf", "/docs", 100, "2026-04-16", registry.get_icon("pdf", "pdf.png", "red")),
        FileEntry("photo.jpg", "/img", 300, "2026-04-16", registry.get_icon("jpg", "image.png", "blue")),
        FileEntry("manual.pdf", "/docs", 200, "2026-04-16", registry.get_icon("pdf", "pdf.png", "red")),
    ]
    print(len(files), registry.count_icons())
    print("-" * 40)

    print("Task 5")
    particle_system = ParticleSystem(ParticleFactory())
    particle_system.emit("spark", 0, 0)
    particle_system.emit("smoke", 1, 1)
    particle_system.update(1.0)
    print(particle_system.render())
